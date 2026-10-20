// Install Google Mobile Ads Unity plugin + UMP, then enable ITME_ADMOB in Player Settings.
#if ITME_ADMOB
using System;using System.Threading;using System.Threading.Tasks;using UnityEngine;using GoogleMobileAds.Api;using GoogleMobileAds.Ump.Api;using ItmeArena.Runtime;
public sealed class ItmeAdMob:MonoBehaviour,IRewardedProvider {
 [Serializable] private sealed class Settings{public string rewardedUnit;}
 private bool ready;private string unit;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]private static void Boot(){var go=new GameObject("Opt-in rewarded ads");DontDestroyOnLoad(go);go.AddComponent<ItmeAdMob>();}
 private void Start(){var source=Resources.Load<TextAsset>("Data/ads");if(source==null)return;unit=JsonUtility.FromJson<Settings>(source.text).rewardedUnit;if(string.IsNullOrWhiteSpace(unit))return;RewardedAds.Provider=this;RewardedAds.PrivacyOptions=PrivacyOptions;MobileAds.RaiseAdEventsOnUnityMainThread=true;}
 public async Task<bool> Show(string intent,CancellationToken token){if(!ready){var consent=new TaskCompletionSource<bool>();ConsentInformation.Update(new ConsentRequestParameters(),error=>{if(error!=null){consent.TrySetResult(false);return;}ConsentForm.LoadAndShowConsentFormIfRequired(e=>consent.TrySetResult(e==null&&ConsentInformation.CanRequestAds()));});if(!await consent.Task)throw new Exception("Reklam izni alınamadı.");var init=new TaskCompletionSource<bool>();MobileAds.Initialize(_=>init.TrySetResult(true));await init.Task;ready=true;}
  token.ThrowIfCancellationRequested();var loaded=new TaskCompletionSource<RewardedAd>();RewardedAd.Load(unit,new AdRequest(),(ad,error)=>{if(error!=null||ad==null)loaded.TrySetException(new Exception("Reklam şu anda hazır değil."));else loaded.TrySetResult(ad);});var rewarded=await loaded.Task;
  try{token.ThrowIfCancellationRequested();if(!rewarded.CanShowAd())return false;rewarded.SetServerSideVerificationOptions(new ServerSideVerificationOptions{CustomData=intent});bool earned=false;var closed=new TaskCompletionSource<bool>();rewarded.OnAdFullScreenContentClosed+=()=>closed.TrySetResult(earned);rewarded.OnAdFullScreenContentFailed+=e=>closed.TrySetException(new Exception("Reklam açılamadı."));rewarded.Show(_=>earned=true);return await closed.Task;}finally{rewarded.Destroy();}}
 public static void PrivacyOptions(){ConsentForm.ShowPrivacyOptionsForm(_=>{});}
}
#endif
