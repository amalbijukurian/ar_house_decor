using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
using System.Collections.Generic;
using TMPro;
using UnityEngine.InputSystem.EnhancedTouch;
using Touch = UnityEngine.InputSystem.EnhancedTouch.Touch;

public class PlaceObject : MonoBehaviour
{
    public ARRaycastManager raycastManager;
    public GameObject objectPrefab; // assign prefab in Inspector
    public TextMeshProUGUI debugText;

    List<ARRaycastHit> hits = new List<ARRaycastHit>();

    void OnEnable()
    {
        EnhancedTouchSupport.Enable();
    }

    void OnDisable()
    {
        EnhancedTouchSupport.Disable();
    }

    void Update()
    {
        if (objectPrefab == null || raycastManager == null)
        {
            SetDebug("Missing prefab or raycast manager!");
            return;
        }

        if (Touch.activeTouches.Count == 0)
        {
            SetDebug("Waiting for touch...");
            return;
        }

        var touch = Touch.activeTouches[0];
        SetDebug("Touch: " + touch.phase);

        if (touch.phase != UnityEngine.InputSystem.TouchPhase.Began) return;

        if (raycastManager.Raycast(touch.screenPosition, hits, TrackableType.PlaneWithinPolygon))
        {
            Pose hitPose = hits[0].pose;
            GameObject obj = Instantiate(objectPrefab, hitPose.position, Quaternion.identity);
            obj.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);
            SetDebug("✅ Object placed!");
        }
        else
        {
            SetDebug("❌ Tap directly on the plane!");
        }
    }

    void SetDebug(string msg)
    {
        if (debugText != null)
            debugText.text = msg;
    }
}