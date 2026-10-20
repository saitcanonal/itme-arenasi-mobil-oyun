from pathlib import Path
import subprocess,tempfile
r=Path(__file__).resolve().parents[1];base=r/'Server/src/main/java/com/itmearena/application';tests=r/'Tools/Standalone'
names=['ArenaPowers','PowerCatalog','NetActions','NetMatch','NetMotion','NetWorld','NetHazards','LobbyRegistry','CompletedMatch','AuthFailure']
with tempfile.TemporaryDirectory() as out:
 files=[str(base/(n+'.java')) for n in names]+[str(x) for x in tests.rglob('*.java')]
 subprocess.run(['java','com.sun.tools.javac.Main','-d',out]+files,check=True)
 for main in ['PowerRulesSmoke','LobbyScopeSmoke']:subprocess.run(['java','-cp',out,'com.itmearena.application.'+main],check=True)
print('Scope: isolated Java gameplay/lobby only. JSON/auth loaders stubbed; Spring, DB and Unity NOT tested.')
