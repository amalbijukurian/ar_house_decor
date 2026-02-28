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
    public ARPlaneManager planeManager;
    public GameObject objectPrefab;
    public TextMeshProUGUI debugText;
    public GameObject deleteButton;

    List<ARRaycastHit> hits = new List<ARRaycastHit>();
    private GameObject selectedObject = null;
    private Camera arCamera;
    private bool objectPlaced = false;

    // Rotation variables
    private float previousAngle = 0f;
    private bool isRotating = false;

    void OnEnable() { EnhancedTouchSupport.Enable(); }
    void OnDisable() { EnhancedTouchSupport.Disable(); }

    void Start()
    {
        arCamera = Camera.main;
        if (deleteButton != null)
            deleteButton.SetActive(false);
        SetPlanesVisible(true);
        SetDebug("🔍 Scanning... point at floor and move slowly");
    }

    void Update()
    {
        if (objectPrefab == null || raycastManager == null) return;

        int planeCount = 0;
        foreach (var plane in planeManager.trackables)
            planeCount++;

        if (!objectPlaced)
            SetDebug("🔍 Planes found: " + planeCount + " - Tap to place!");

        // TWO FINGER ROTATION
        if (Touch.activeTouches.Count == 2 && selectedObject != null)
        {
            var touch0 = Touch.activeTouches[0];
            var touch1 = Touch.activeTouches[1];

            float currentAngle = GetAngleBetweenTouches(touch0.screenPosition, touch1.screenPosition);

            if (!isRotating)
            {
                previousAngle = currentAngle;
                isRotating = true;
            }
            else
            {
                float angleDiff = currentAngle - previousAngle;
                selectedObject.transform.Rotate(0, -angleDiff, 0);
                previousAngle = currentAngle;
                SetDebug("🔄 Rotating object...");
            }
            return;
        }
        else
        {
            isRotating = false;
        }

        if (Touch.activeTouches.Count == 0) return;

        var touch = Touch.activeTouches[0];

        // DRAG to move selected object
        if (touch.phase == UnityEngine.InputSystem.TouchPhase.Moved && selectedObject != null)
        {
            if (raycastManager.Raycast(touch.screenPosition, hits, TrackableType.PlaneWithinPolygon))
            {
                selectedObject.transform.position = hits[0].pose.position;
                SetDebug("↔️ Moving object...");
            }
            return;
        }

        if (touch.phase != UnityEngine.InputSystem.TouchPhase.Began) return;

        // CHECK if tapping existing object
        Ray ray = arCamera.ScreenPointToRay(touch.screenPosition);
        RaycastHit hitInfo;
        if (Physics.Raycast(ray, out hitInfo))
        {
            SelectObject(hitInfo.collider.gameObject);
            SetDebug("✅ Selected! Drag to move, 2 fingers to rotate.");
            return;
        }

        // PLACE new object
        if (raycastManager.Raycast(touch.screenPosition, hits, TrackableType.PlaneWithinPolygon))
        {
            Pose hitPose = hits[0].pose;
            GameObject obj = Instantiate(objectPrefab, hitPose.position, Quaternion.identity);
            obj.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);

            if (obj.GetComponent<Collider>() == null)
                obj.AddComponent<BoxCollider>();

            objectPlaced = true;
            SetPlanesVisible(false);
            DeselectObject();
            SetDebug("✅ Placed! Tap object to select.");
        }
        else
        {
            SetDebug("❌ No plane found - keep scanning floor");
        }
    }

    float GetAngleBetweenTouches(Vector2 pos0, Vector2 pos1)
    {
        Vector2 direction = pos1 - pos0;
        return Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg;
    }

    void SetPlanesVisible(bool visible)
    {
        foreach (var plane in planeManager.trackables)
        {
            var mr = plane.GetComponent<MeshRenderer>();
            var lr = plane.GetComponent<LineRenderer>();
            if (mr != null) mr.enabled = visible;
            if (lr != null) lr.enabled = visible;
        }

        planeManager.planesChanged += (args) =>
        {
            foreach (var plane in args.added)
            {
                var mr = plane.GetComponent<MeshRenderer>();
                var lr = plane.GetComponent<LineRenderer>();
                if (mr != null) mr.enabled = visible;
                if (lr != null) lr.enabled = visible;
            }
        };
    }

    void SelectObject(GameObject obj)
    {
        if (selectedObject != null) DeselectObject();
        selectedObject = obj;

        var renderer = selectedObject.GetComponentInChildren<Renderer>();
        if (renderer != null)
            renderer.material.color = new Color(0.5f, 0.8f, 1f);

        if (deleteButton != null)
            deleteButton.SetActive(true);
    }

    void DeselectObject()
    {
        if (selectedObject != null)
        {
            var renderer = selectedObject.GetComponentInChildren<Renderer>();
            if (renderer != null)
                renderer.material.color = Color.white;
        }
        selectedObject = null;
        if (deleteButton != null)
            deleteButton.SetActive(false);
    }

    public void DeleteSelected()
    {
        if (selectedObject != null)
        {
            Destroy(selectedObject);
            selectedObject = null;
            if (deleteButton != null)
                deleteButton.SetActive(false);
            objectPlaced = false;
            SetPlanesVisible(true);
            SetDebug("🔍 Scanning for planes...");
        }
    }

    void SetDebug(string msg)
    {
        if (debugText != null)
            debugText.text = msg;
    }
}