#!/usr/bin/env python3
"""P19 structural validation; NOT Unity compilation or gameplay testing."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'UnityProject/Assets'

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def validate_catalog(c, source_ids):
    require(c['schemaVersion'] == 1, 'Unsupported catalog version')
    for group in ['characters', 'maps', 'accessories', 'parameters']:
        ids = [x['id'] for x in c[group]]
        require(len(ids) == len(set(ids)), 'Duplicate ID: ' + group)
        require(all(re.fullmatch('[a-z][a-z0-9_]*', x) for x in ids), 'Invalid ID')
        require(all(x['sourceId'] in source_ids for x in c[group]), 'Unknown source')
    chars = {x['id']: x for x in c['characters']}
    accessories = {x['id']: x for x in c['accessories']}
    for a in accessories.values():
        require(a['characterId'] in chars, 'Dangling accessory owner')
        require(a['id'] in chars[a['characterId']]['accessoryIds'], 'Unlisted accessory')
        require(a['examplePrice'] >= 2000, 'Below minimum example price')
        require(a['artStatus'] == 'accessory-v1-runtime-unverified' and a['assetKey'] == 'Accessories/'+a['id'], 'P01 art claim')
    for char in chars.values():
        require(len(char['accessoryIds']) == len(set(char['accessoryIds'])), 'Repeated equipped slot reference')
        for aid in char['accessoryIds']:
            require(aid in accessories and accessories[aid]['characterId'] == char['id'], 'Invalid accessory relation')
        require((char['artStatus'] == 'rigged-v1-runtime-unverified' and char['assetKey'] == 'Characters/'+char['id']) if char['id'] in ['pofuk','cengel','kivilcim','firtina','koli_kenan'] else (char['artStatus'] == 'not-produced' and char['assetKey'] == ''), 'Character art scope claim')
    for m in c['maps']:
        require(sorted(m['supportedPlayerCounts']) == [2, 4], 'Invalid player counts')
        require((m['sceneName'] == 'Boot' and m['implementationStatus'] == 'runtime-built-unverified') if m['id'] in ['merdiven_boslugu','kirik_fabrika','kizil_krater'] else (m['sceneName'] == '' and m['implementationStatus'] == 'definition-only'), 'P01 map claim')
    require(len(chars) == 5 and len(c['maps']) == 3 and len(accessories) == 26, 'Reference counts differ')

def validate_schema_subset(value, schema, at='$'):
    """Only the keywords used in this project's schema; not a full JSON Schema engine."""
    if 'const' in schema:
        require(value == schema['const'], at + ': const mismatch')
    if 'enum' in schema:
        require(value in schema['enum'], at + ': enum mismatch')
    kind = schema.get('type')
    if kind == 'object':
        require(isinstance(value, dict), at + ': expected object')
        require(all(k in value for k in schema.get('required', [])), at + ': required key missing')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            require(set(value) <= set(props), at + ': unexpected key')
        for k, v in value.items():
            if k in props:
                validate_schema_subset(v, props[k], at + '.' + k)
    elif kind == 'array':
        require(isinstance(value, list), at + ': expected array')
        require(len(value) >= schema.get('minItems', 0), at + ': too short')
        if schema.get('uniqueItems'):
            encoded = [json.dumps(x, sort_keys=True) for x in value]
            require(len(set(encoded)) == len(encoded), at + ': duplicate item')
        for i, v in enumerate(value):
            validate_schema_subset(v, schema.get('items', {}), at + '[' + str(i) + ']')
    elif kind == 'string':
        require(isinstance(value, str), at + ': expected string')
        require(len(value) >= schema.get('minLength', 0), at + ': empty string')
        if 'pattern' in schema:
            require(re.search(schema['pattern'], value) is not None, at + ': pattern')
    elif kind in ['integer', 'number']:
        require(type(value) in ([int] if kind == 'integer' else [int, float]), at + ': expected number')
        if 'minimum' in schema:
            require(value >= schema['minimum'], at + ': below minimum')
        if 'maximum' in schema:
            require(value <= schema['maximum'], at + ': above maximum')


def main():
    checks = []
    sources = load('References/sources.json')
    require(len(sources) == 11, 'Expected eleven sources')
    source_ids = {s['id'] for s in sources}
    require(len(source_ids) == 11, 'Duplicate source IDs')
    for s in sources:
        file = ROOT / s['path']
        require(file.is_file(), 'Missing source PDF')
        require(hashlib.sha256(file.read_bytes()).hexdigest() == s['sha256'], 'Source PDF changed: ' + s['id'])
    checks.append('11 source PDFs and SHA-256 hashes')
    catalog = load('UnityProject/Assets/ItmeArena/Resources/Data/catalog.json')
    validate_catalog(catalog, source_ids)
    schema = load('Contracts/catalog.schema.json')
    validate_schema_subset(catalog, schema)
    checks.append('Catalog satisfies the schema keywords used (bundled subset checker, not full JSON Schema engine)')
    checks.append('5 characters / 3 maps / 26 accessories; ownership and source relations')
    # Negative checks make sure the acceptance gate actually detects corrupt catalogs.
    mutations = [lambda c: c['characters'].append(copy.deepcopy(c['characters'][0])),
                 lambda c: c['accessories'][0].update(characterId='missing'),
                 lambda c: c['maps'][0].update(sourceId='S99'),
                 lambda c: c['maps'][0].update(supportedPlayerCounts=[2]),
                 lambda c: c['accessories'][0].update(examplePrice=-1)]
    for mutate in mutations:
        corrupt = copy.deepcopy(catalog)
        mutate(corrupt)
        try:
            validate_catalog(corrupt, source_ids)
        except ValueError:
            continue
        raise ValueError('Corrupt catalog accepted')
    checks.append('5 negative cases rejected: duplicate, dangling owner, source, counts, price')
    metas = {}
    for p in ASSETS.rglob('*'):
        if p.suffix == '.meta':
            continue
        meta = Path(str(p) + '.meta')
        require(meta.is_file(), 'Missing .meta: ' + str(p))
        match = re.search(r'^guid: ([0-9a-f]{32})$', meta.read_text(), re.M)
        require(match is not None, 'Invalid GUID')
        require(match[1] not in metas, 'Duplicate GUID')
        metas[match[1]] = p
    for p in ASSETS.rglob('*.unity'):
        text = p.read_text()
        for g in re.findall(r'guid: ([0-9a-f]{32})', text):
            require(g in metas, 'Scene reference cannot resolve')
        ids = set(re.findall(r'^--- !u!\d+ &(\d+)', text, re.M))
        for line in text.splitlines():
            if 'guid:' not in line:
                for fid in re.findall(r'fileID: (\d+)', line):
                    require(fid == '0' or fid in ids, 'Dangling scene fileID')
        require('orthographic: 1' in text, 'Not an orthographic 2D camera')
    build = (ROOT/'UnityProject/ProjectSettings/EditorBuildSettings.asset').read_text()
    for g in re.findall(r'guid: ([0-9a-f]{32})', build):
        require(g in metas and metas[g].suffix == '.unity', 'Build scene GUID missing')
    checks.append('All Unity assets have unique .meta; scene local/script/build references resolve')
    settings=(ROOT/'UnityProject/ProjectSettings/ProjectSettings.asset').read_text()
    require('defaultScreenOrientation: 3' in settings, 'Landscape default missing')
    require('allowedAutorotateToPortrait: 0' in settings, 'Portrait enabled')
    defs=[json.loads(p.read_text()) for p in ASSETS.rglob('*.asmdef')]
    names={d['name'] for d in defs}
    require(len(names)==3,'Assembly boundary count')
    for d in defs:
        require(all(ref in names or ref == 'UnityEngine.UI' for ref in d['references']), 'Unresolved assembly reference')
    core=next(d for d in defs if d['name']=='ItmeArena.Core')
    require(core['noEngineReferences'] and core['references']==[], 'Core engine coupling')
    for cs in (ASSETS/'ItmeArena/Core').glob('*.cs'):
        require('UnityEngine' not in cs.read_text() and 'UnityEditor' not in cs.read_text(), 'Core imports engine')
    checks.append('Landscape settings and three assembly boundaries')
    reqs=load('Docs/requirements.json')
    require(len({r['id'] for r in reqs})==len(reqs),'Duplicate requirement ID')
    require(set(r['stage'] for r in reqs)==set(range(1,33)), 'Stage coverage gap')
    require(all(r['status']=='bekliyor' for r in reqs if r['stage']>32), 'Later stage marked done')
    for name in ['README_TR','V1_KAPSAM','ILERLEME','KARARLAR','HATALAR','TESTLER','DEGISIKLIKLER','SONRAKI_ADIM']:
        require((ROOT/(name+'.md')).is_file(), 'Required record missing: '+name)
    checks.append(str(len(reqs))+' requirements cover stages 01–32; later stages pending; eight records exist')
    for p in ROOT.rglob('*.json'):
        json.loads(p.read_text())
    checks.append('All JSON files parse')
    manifest=load('UnityProject/Packages/manifest.json')['dependencies']
    require(manifest.get('com.unity.ugui') == '2.0.0', 'uGUI package not pinned')
    config=load('UnityProject/Assets/ItmeArena/Resources/Data/onboarding.json')
    require(config['developmentScenario'] in ['Success','Offline','ServiceError','Timeout','InvalidResponse','SaveError'], 'Invalid test scenario')
    require(100 <= config['timeoutMs'] <= 60000, 'Unsafe timeout')
    require(config['simulatedDelayMs'] >= 0, 'Invalid delay')
    require(isinstance(config['exactBlocked'], list) and isinstance(config['blockedFragments'], list), 'Invalid moderation lists')
    checks.append('uGUI package and onboarding scenario/configuration values')
    movement=load('UnityProject/Assets/ItmeArena/Resources/Data/movement.json')
    require(all(isinstance(v, (float,int)) and v >= 0 for v in movement.values()), 'Invalid movement settings')
    require(0 < movement['airControl'] <= 1 and 0 < movement['crouchMultiplier'] <= 1, 'Movement multiplier')
    require(movement['standingHeight'] > movement['crouchingHeight'] > movement['skin']*4, 'Crouch shape invalid')
    require(0 < movement['jumpBuffer'] <= 1 and 0 < movement['coyoteTime'] <= 1, 'Movement time windows')
    checks.append('P04 movement configuration and dimensions (structural only)')
    push=load('UnityProject/Assets/ItmeArena/Resources/Data/push.json')
    require(push['friendlyFire'] is False, 'Default friendly fire must be disabled')
    require(push['damage'] > 0 and push['range'] > 0 and push['cooldown'] > 0, 'Invalid attack settings')
    require(push['recovery'] > push['maxImpulse']/push['impulseDecay'], 'No guaranteed recovery window')
    require('executionOrder: 100' in (ASSETS/'ItmeArena/Runtime/PushCombatWorld.cs.meta').read_text(), 'Combat must resolve after all motors')
    checks.append('P05 attack settings, friendly-fire default, recovery window, execution order')
    grip=load('UnityProject/Assets/ItmeArena/Resources/Data/grip.json')
    require(0 <= grip['resumeFatigue'] < grip['warningFatigue'] < 1, 'Invalid fatigue thresholds')
    require(grip['restDelay'] >= 0 and grip['fatigueRate'] > 0 and grip['recoveryRate'] > 0, 'Invalid fatigue rates')
    require(grip['pulseWindow'] > 0 and grip['reach'] > 0 and 1 <= grip['maxChain'] <= 16, 'Grip pulse/range/chain')
    require(grip['followSpeed'] >= grip['climbSpeed'] > 0 and grip['maxStretch'] >= grip['reach'], 'Grip movement limits')
    checks.append('P06 fatigue, pulse, recovery and finite chain configuration')
    match=load('UnityProject/Assets/ItmeArena/Resources/Data/match.json')
    require(match['durationSeconds'] == 120 and match['countdownSeconds'] >= 0, 'Match duration/countdown')
    require(match['equalSurvivorsAfterFalls'] == 'Draw', 'Temporary equal-survivor default must be draw')
    require('executionOrder: -200' in (ASSETS/'ItmeArena/Runtime/MatchController.cs.meta').read_text(), 'Match phase gate must precede movement/combat')
    checks.append('P07 120-second default, countdown, draw policy and pre-motor execution order')
    print('P19 STRUCTURAL VALIDATION: PASS')
    for c in checks:
        print('PASS: '+c)
    print('NOT TESTED: Unity import, C# compilation, Play Mode, Android build, device and visual QA')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as exc:
        print('P19 STRUCTURAL VALIDATION: FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
