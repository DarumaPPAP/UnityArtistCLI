using NUnit.Framework;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityArtist;

namespace UnityCi {
 public class PipelineSmokeTests {
  RenderPipelineAsset previousGraphics, previousQuality;
  [SetUp] public void OpenConcreteSceneAndConfigurePipeline() {
   previousGraphics = GraphicsSettings.defaultRenderPipeline; previousQuality = QualitySettings.renderPipeline;
   EditorSceneManager.OpenScene("Assets/Scenes/PipelineSmoke.unity");
   GraphicsSettings.defaultRenderPipeline = null; QualitySettings.renderPipeline = null;
  }
  [TearDown] public void RestorePipeline() {
   GraphicsSettings.defaultRenderPipeline = previousGraphics; QualitySettings.renderPipeline = previousQuality;
   AssetDatabase.DeleteAsset("Assets/CiPipeline.asset"); AssetDatabase.DeleteAsset("Assets/CiRenderer.asset");
  }
  [Test] public void SceneContainsCameraLightAndRenderableSubject() {
   Assert.IsNotNull(Camera.main); Assert.IsNotNull(Object.FindFirstObjectByType<Light>());
   var subject = GameObject.Find("FovSubject"); Assert.IsNotNull(subject);
   Assert.IsNotNull(subject.GetComponent<MeshRenderer>()); Assert.IsNotNull(subject.GetComponent<MeshFilter>().sharedMesh);
   Assert.IsTrue(ArtistCompatibility.IsSupported(Application.unityVersion, "builtin"));
  }
  [Test] public void NativePipelineSettingsCanBeConfigured() { Assert.IsNull(GraphicsSettings.defaultRenderPipeline); RenderSettings.fog = true; RenderSettings.fogDensity = 0.03f; Assert.AreEqual(0.03f, RenderSettings.fogDensity); }
 }
}
