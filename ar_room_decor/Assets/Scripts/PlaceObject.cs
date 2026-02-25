using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
using System.Collections.Generic;
using GLTFast;
using System.Threading.Tasks;

public class PlaceObject : MonoBehaviour
{
    public ARRaycastManager raycastManager;
    public GameObject loadedModel;
    private bool modelLoaded = false;

    List<ARRaycastHit> hits = new List<ARRaycastHit>();

    async void Start()
    {
        await LoadModel();
    }

    async Task LoadModel()
    {
        if (loadedModel != null)
        {
            modelLoaded = true;
            return;
        }
        string glbPath = "file://" + Application.dataPath + "/Models/Study Table.glb";
        var gltfImport = new GltfImport();
        bool success = await gltfImport.Load(glbPath);
        if (success)
        {
            // Create a container for the model
            GameObject modelContainer = new GameObject("StudyTable");
            await gltfImport.InstantiateMainSceneAsync(modelContainer.transform);
            loadedModel = modelContainer;
            modelLoaded = true;
            Debug.Log("Model loaded successfully!");
        }
        else
        {
            Debug.LogError("Failed to load model!");
        }
        gltfImport.Dispose();
    }

    void Update()
    {
        if (!modelLoaded) return;

        bool mousePressed = Input.GetMouseButtonDown(0);

        if (Input.touchCount == 0 && !mousePressed) return;

        Touch touch = new Touch();
        if (!mousePressed)
        {
            touch = Input.GetTouch(0);
            if (touch.phase != TouchPhase.Began) return;
        }

        Vector3 pos = mousePressed?Input.mousePosition:touch.position;

        if (raycastManager.Raycast(pos, hits, TrackableType.PlaneWithinPolygon))
        {
            Pose hitPose = hits[0].pose;
            Instantiate(loadedModel, hitPose.position, Quaternion.identity);
            Debug.Log("Object Placed!");
        }
    }
}