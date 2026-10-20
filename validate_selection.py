"""P14 asset/routing/layout/source checks, NOT C# or Unity execution."""
from pathlib import Path
from PIL import Image
import hashlib,re
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
ids=['merdiven_boslugu','kirik_fabrika','kizil_krater'];hashes=[]
for id in ids:
 p=A/('Resources/MapPreviews/'+id+'.png');im=Image.open(p);assert im.size==(1536,864);im.verify();hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
 assert 'textureType: 8' in Path(str(p)+'.meta').read_text();assert (R/('ArtSource/P14/'+id+'.svg')).is_file()
assert len(set(hashes))==3
screen=(A/'Runtime/SelectionScreen.cs').read_text();menu=(A/'Runtime/MainMenuScreen.cs').read_text();lab=(A/'Runtime/MovementLab.cs').read_text();core=(A/'Core/Selection.cs').read_text()
for id in ids:assert id in menu and id in lab and id in screen and id in core
for token in ['draft.CreateLaunch()','if(launching||closing||!mapConfirmed)return','draft.CanMove(index)','draft.SetConsent','draft.BlockReason()']:assert token in screen,token
for token in ['OpenSelection(2,false)','OpenSelection(4,false)','selectionScreen?.Resume()','Time.frameCount==resumedFrame']:assert token in menu,token
for token in ['selectedRoster[i].Team','selectionRequest.SpawnIndexFor(i)','Selection/map route mismatch']:assert token in lab,token
assert 'RoomNumber=>null' in core and 'if(OnlinePreview)return' in core
assert 200+2*300+280<=1194 and 380+2*80+74<=634
assert 330+286+60<=720
# A small lexical gate catches accidentally inserted literal newlines in C# strings, not type/API errors.
for file in ['Runtime/CurrencyShop.cs','Runtime/RewardedAds.cs','Runtime/WardrobeTab.cs','Runtime/WelcomeArrival.cs','Runtime/MenuBrandArt.cs','Runtime/MatchControlArt.cs','Runtime/MatchEndAnnouncement.cs','Runtime/ArenaSettingsPanel.cs','Runtime/MatchNotice.cs','Runtime/MatchPauseMenu.cs','Runtime/ControlLayoutEditor.cs','Runtime/HoldControl.cs','Runtime/CartoonArenaMotion.cs','Runtime/MenuHeroGreeting.cs','Runtime/ModeCardMotion.cs','Runtime/ArenaButtonSkin.cs','Runtime/ArenaTheme.cs','Runtime/StudioPanel.cs','Runtime/ArenaProgressPanel.cs','Editor/MapPickerChecks.cs','Runtime/MapPicker.cs','Editor/ReleaseBuildTools.cs','Runtime/PlatformHaptics.cs','Runtime/VisualCapture.cs','Editor/VisualCaptureTools.cs','Runtime/MatchResultScreen.cs','Runtime/FlowDiagnostics.cs','Runtime/ShopClient.cs','Runtime/RewardStatusView.cs','Runtime/NetworkWorld.cs','Runtime/NetworkMotion.cs','Runtime/OnlineArena.cs','Runtime/LobbyPanel.cs','Runtime/LobbyTransport.cs','Runtime/ProductionRegistrationService.cs','Runtime/SecureSessionStore.cs','Runtime/ServerApiClient.cs','Runtime/MobileQuality.cs','Runtime/MobileMetrics.cs','Editor/MobileBuildTools.cs','Editor/StorageChecks.cs','Runtime/SqliteConnection.cs','Runtime/LocalCache.cs','Runtime/FoundationBoot.cs','Runtime/FirstLaunchScreen.cs','Runtime/CharacterCustomizationScreen.cs','Runtime/ArenaAudio.cs','Runtime/ArenaFeedback.cs','Runtime/ArenaAtmosphere.cs','Core/DragClaims.cs','Core/Grip.cs','Runtime/GripController.cs','Runtime/StunVisual.cs','Runtime/CharacterVisual.cs','Editor/DragChecks.cs','Core/Ultimate.cs','Editor/UltimateChecks.cs','Runtime/UltimateWorld.cs','Runtime/CharacterMotor.cs','Runtime/PushCombatWorld.cs','Core/BotRules.cs','Editor/BotChecks.cs','Runtime/BotController.cs','Runtime/StairwellArena.cs','Runtime/FactoryArena.cs','Runtime/CraterArena.cs','Core/Selection.cs','Editor/SelectionChecks.cs','Runtime/SelectionScreen.cs','Runtime/MainMenuScreen.cs','Runtime/MovementLab.cs']:
 s=(A/file).read_text();i=0;stack=[]
 while i<len(s):
  if s.startswith('//',i):
   end=s.find('\n',i);i=len(s) if end<0 else end+1;continue
  if s.startswith('/*',i):
   end=s.find('*/',i+2);assert end>=0;i=end+2;continue
  if s[i] in ['"',"'"]:
   quote=s[i];i+=1
   while i<len(s) and s[i]!=quote:
    assert s[i]!='\n',('newline inside literal',file)
    i+=2 if s[i]=='\\' else 1
   assert i<len(s);i+=1;continue
  if s[i] in '({[':stack.append(s[i])
  elif s[i] in ')}]':assert stack and stack.pop()==dict(zip(')}]','({['))[s[i]],file
  i+=1
 assert not stack,file
print('PASS: three distinct 1536x864 sprite thumbnails and editable SVG sources')
print('PASS: 2/4 local and room-preview routes, map/team/spawn forwarding, launch lock and return-frame guard (source checks)')
print('PASS: three modal map buttons and three rows per team fit source layout; C# literal/delimiter lexical gate')
print('NOT RUN: SelectionChecks, C# compilation, Unity UI/import/input/back navigation, live room service or Android acceptance')
