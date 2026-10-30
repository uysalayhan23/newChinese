#!/usr/bin/env python3
"""Review-only REAL MainActivity -> HSK6 -> SC042/048 navigation smoke.

Requires booted Android emulator and installed debug APK. Does not launch the
review probe; never treats splash, PID-only or missing UI hierarchy as PASS.
"""
import argparse
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from hsk6_review_evidence_gate import validate_pixels

PKG = 'com.uysal23.newchinese'
TITLES = {'042': 'Dil yaşamda neyi değiştirdi', '048': 'Gelecekte de hata yapmak'}
BOUNDS = re.compile(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]')


def position(xml, text, prefix=False):
    root = ET.fromstring(xml)
    parents = {n: p for p in root.iter() for n in p}
    for n in root.iter('node'):
        if n.get('visible-to-user') == 'false':
            continue
        labels = (n.get('text', ''), n.get('content-desc', ''))
        if not any(x.startswith(text) if prefix else x == text for x in labels):
            continue
        target = n
        disabled = target.get('enabled') == 'false'
        while target in parents and target.get('clickable') != 'true':
            target = parents[target]
            disabled = disabled or target.get('enabled') == 'false'
        # A locked scene row still has text and bounds in UIAutomator.
        # Never treat tapping its disabled button as a successful navigation.
        if disabled or target.get('enabled') == 'false':
            continue
        match = BOUNDS.fullmatch(target.get('bounds', '')) or BOUNDS.fullmatch(n.get('bounds', ''))
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            if x2 > x1 and y2 > y1:
                return (x1+x2)//2, (y1+y2)//2
    return None


def visual_bounds(xml, scene, screen, title):
    root = ET.fromstring(xml)
    if screen == 'intro':
        nodes = [n for n in root.iter('node') if n.get('content-desc') == title]
    else:
        nodes = [n for n in root.iter('node') if re.fullmatch(
            rf'SC{scene}_REVIEW_READY_(ZHANG|LI)', n.get('content-desc', ''))]
    if len(nodes) != 1 or nodes[0].get('visible-to-user') == 'false':
        raise AssertionError(f'SC{scene} {screen}: verified visual marker missing/ambiguous')
    match = BOUNDS.fullmatch(nodes[0].get('bounds', ''))
    if not match:
        raise AssertionError(f'SC{scene} {screen}: missing visual bounds')
    x1, y1, x2, y2 = map(int, match.groups())
    if x2 - x1 < 300 or y2 - y1 < 300:
        raise AssertionError(f'SC{scene} {screen}: unusable visual bounds')
    return x1, y1, x2, y2


def crashed(log):
    # A process can restart before capture(), so pidof alone does not prove
    # the scene was crash-free. Event logs also report crashes and ANRs
    # without a Java "Process:" stacktrace.
    return bool(
        re.search(r'\bProcess:\s*' + re.escape(PKG) + r'(?=[,:\s]|$)', log)
        or re.search(r'(?m)^[^\n]*\bam_(?:crash|anr)\b[^\n]*\b'
                     + re.escape(PKG) + r'(?=[,:\s\]]|$)', log)
    )


class Android:
    def __init__(self, out):
        self.out = Path(out)
        self.out.mkdir(parents=True, exist_ok=True)
        self.xml = ''

    def adb(self, *args, binary=False, timeout=40):
        p = subprocess.run(['adb', *args], check=True, capture_output=True, timeout=timeout)
        return p.stdout if binary else p.stdout.decode(errors='replace')

    def dump(self):
        self.adb('shell', 'uiautomator', 'dump', '/sdcard/nc-navigation.xml')
        self.xml = self.adb('exec-out', 'cat', '/sdcard/nc-navigation.xml')
        ET.fromstring(self.xml)
        return self.xml

    def alive(self):
        try:
            return bool(self.adb('shell', 'pidof', PKG).strip())
        except subprocess.CalledProcessError:
            return False

    def wait(self, *labels, timeout=75, prefix=False):
        until = time.monotonic() + timeout
        while time.monotonic() < until:
            try:
                xml = self.dump()
                if self.alive() and any(position(xml, x, prefix=prefix) for x in labels):
                    return xml
            except (subprocess.SubprocessError, ET.ParseError):
                pass
            time.sleep(2)
        raise AssertionError(f'App did not show {labels!r}')

    def tap(self, text, prefix=False, scroll=False):
        for _ in range(19 if scroll else 1):
            p = position(self.dump(), text, prefix)
            if p:
                self.adb('shell', 'input', 'tap', str(p[0]), str(p[1]))
                time.sleep(1)
                return
            if scroll:
                self.adb('shell', 'input', 'swipe', '540', '1740', '540', '470', '360')
        raise AssertionError(f'Cannot tap {text!r}')

    def capture(self, name, scene=None, screen=None, title=None):
        self.dump()
        bounds = visual_bounds(self.xml, scene, screen, title) if scene else None
        (self.out / (name+'.xml')).write_text(self.xml)
        png = self.adb('exec-out', 'screencap', '-p', binary=True)
        (self.out / (name+'.png')).write_bytes(png)
        log = self.adb('logcat', '-d')
        (self.out / (name+'_logcat.txt')).write_text(log)
        if not png.startswith(b'\x89PNG\r\n\x1a\n') or len(png) < 5000:
            raise AssertionError(f'{name}: invalid screenshot')
        if bounds is not None:
            validate_pixels(self.out / (name+'.png'), bounds=bounds)
        if crashed(log) or not self.alive():
            raise AssertionError(f'{name}: application exited/crashed')


def run(out):
    d = Android(out)
    try:
        d.adb('shell', 'am', 'force-stop', PKG)
        d.adb('logcat', '-c')
        d.adb('shell', 'am', 'start', '-n', PKG+'/.MainActivity')
        xml = d.wait('Adın nedir?', 'HSK Seviyeleri')
        if position(xml, 'Adın nedir?'):
            d.tap('Kullanıcı adı')
            d.adb('shell', 'input', 'text', 'QA')
            d.adb('shell', 'input', 'keyevent', '4')
            d.tap('Devam Et')
        d.wait('HSK Seviyeleri')
        d.tap('Ayarlar')
        d.wait('Ayarlar')
        for _ in range(12):
            xml = d.dump()
            if position(xml, 'Admin modu açık.', True):
                break
            if position(xml, 'Admin şifresi'):
                d.tap('Admin şifresi')
                d.adb('shell', 'input', 'text', 'HSK2026')
                d.adb('shell', 'input', 'keyevent', '4')
                d.tap('Admin Modunu Aç', scroll=True)
                d.wait('Admin modu açıldı.')
                break
            d.adb('shell', 'input', 'swipe', '540', '1740', '540', '470', '360')
        else:
            raise AssertionError('Admin access not found')
        d.tap('Ana Sayfa')
        d.wait('HSK Seviyeleri')
        d.tap('HSK Seviyeleri')
        d.wait('HSK Seviyeleri')
        d.tap('HSK6 ·', prefix=True)
        d.wait('Sahne ', prefix=True)
        for scene, title in TITLES.items():
            d.tap('Sahne '+str(int(scene))+' ·', prefix=True, scroll=True)
            # The 220dp preview, metadata and summary can push the start
            # button below the viewport. Verify the exact intro title first,
            # capture the visible scene, then scroll to its enabled action.
            xml = d.wait(title)
            if not position(xml, title):
                raise AssertionError(f'SC{scene}: intro title mismatch')
            d.capture('sc'+scene+'_normal_intro', scene, 'intro', title)
            d.tap('Diyaloğu Başlat', scroll=True)
            until = time.monotonic()+75
            while time.monotonic() < until:
                xml = d.dump()
                texts = [n.get('text','') for n in ET.fromstring(xml).iter('node')]
                if d.alive() and position(xml,title) and any(re.fullmatch(r'\d+ / 36',x) for x in texts):
                    break
                time.sleep(2)
            else:
                raise AssertionError(f'SC{scene}: dialogue missing')
            d.capture('sc'+scene+'_normal_dialogue', scene, 'dialogue', title)
            d.adb('shell', 'input', 'keyevent', '4')
            d.wait('Diyaloğu Başlat')
            d.adb('shell', 'input', 'keyevent', '4')
            d.wait('Sahne ', prefix=True)
        print('SC042/048 normal navigation intro+dialogue 4/4 PASS')
    except Exception:
        try:
            (d.out/'failure_logcat.txt').write_text(d.adb('logcat','-d'))
            (d.out/'failure.png').write_bytes(d.adb('exec-out','screencap','-p',binary=True))
            (d.out/'failure.xml').write_text(d.dump())
        except Exception:
            pass
        raise


def selftest():
    xml = '<hierarchy><node clickable="true" bounds="[0,0][100,100]"><node text="Diyaloğu Başlat" bounds="[10,10][30,30]"/></node></hierarchy>'
    assert position(xml,'Diyaloğu Başlat') == (50,50)
    assert position(xml,'Diyaloğu',prefix=True) == (50,50)
    assert position(xml,'Sahne 42 ·',prefix=True) is None
    splash = '<hierarchy><node text="NewChinese" bounds="[0,0][100,100]"/></hierarchy>'
    assert position(splash,'Diyaloğu Başlat') is None
    assert crashed('FATAL EXCEPTION: main\nProcess: '+PKG+', PID: 12')
    assert not crashed('FATAL EXCEPTION: main\nProcess: com.android.launcher, PID: 12')
    assert crashed('I am_crash: [0,1234,'+PKG+',12345,IllegalStateException]')
    assert crashed('I am_anr: [0,1234,'+PKG+',Input dispatching timed out]')
    assert not crashed('I am_crash: [0,1234,com.android.launcher,12345,RuntimeException]')
    assert not crashed('I am_crash: [0,1234,'+PKG+'plus,12345,RuntimeException]')
    assert not crashed('OtherProcess: '+PKG)
    assert TITLES['042'] != TITLES['048']
    # Intro action may be offscreen even though the correct scene loaded.
    intro_top = '<hierarchy><node text="'+TITLES['042']+'" bounds="[0,0][200,40]"/></hierarchy>'
    assert position(intro_top, TITLES['042']) == (100,20)
    assert position(intro_top, 'Diyaloğu Başlat') is None
    locked = '<hierarchy><node clickable="true" enabled="false" bounds="[0,0][100,100]"><node text="Sahne 42 · Kilitli" enabled="false" bounds="[10,10][30,30]"/></node></hierarchy>'
    assert position(locked, 'Sahne 42 ·', prefix=True) is None
    assert position(locked.replace('enabled="false"', 'enabled="true"'), 'Sahne 42 ·', prefix=True) == (50, 50)
    scene_list = '<hierarchy><node clickable="true" bounds="[0,0][100,100]"><node text="Sahne 42 · Dil yaşamda neyi değiştirdi" bounds="[10,10][30,30]"/></node></hierarchy>'
    assert position(scene_list, 'Sahne ', prefix=True) == (50, 50)
    assert position(scene_list, 'HSK6') is None
    intro_visual = '<hierarchy><node content-desc="' + TITLES['042'] + '" bounds="[0,0][500,500]"/></hierarchy>'
    dialogue_visual = '<hierarchy><node content-desc="SC042_REVIEW_READY_ZHANG" bounds="[0,0][500,500]"/></hierarchy>'
    assert visual_bounds(intro_visual, '042', 'intro', TITLES['042']) == (0, 0, 500, 500)
    assert visual_bounds(dialogue_visual, '042', 'dialogue', TITLES['042']) == (0, 0, 500, 500)
    invalid_visuals = (
        dialogue_visual.replace('SC042_REVIEW_READY_ZHANG', 'SC048_REVIEW_READY_ZHANG'),
        dialogue_visual.replace('SC042_REVIEW_READY_ZHANG', 'SC042_NOT_READY_ZHANG'),
        dialogue_visual.replace('[0,0][500,500]', '[0,0][2,2]'),
        dialogue_visual.replace('content-desc=', 'visible-to-user="false" content-desc='),
        dialogue_visual.replace('</hierarchy>', '<node content-desc="SC042_REVIEW_READY_LI" bounds="[0,0][500,500]"/></hierarchy>'),
    )
    for invalid in invalid_visuals:
        try:
            visual_bounds(invalid, '042', 'dialogue', TITLES['042'])
        except AssertionError:
            pass
        else:
            raise AssertionError('Invalid scene marker accepted')
    print('Normal navigation static positive/negative self-test 25/25 PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',default='qa-screens/normal-navigation')
    parser.add_argument('--self-test',action='store_true')
    args = parser.parse_args()
    try:
        selftest() if args.self_test else run(args.out)
    except Exception as exc:
        print('NOT PASS:',exc,file=sys.stderr)
        sys.exit(1)
