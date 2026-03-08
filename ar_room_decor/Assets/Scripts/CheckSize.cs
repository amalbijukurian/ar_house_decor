using UnityEngine;

public class CheckSize : MonoBehaviour
{
    void Start()
    {
        Renderer[] renderers = GetComponentsInChildren<Renderer>();
        Bounds bounds = new Bounds(transform.position, Vector3.zero);
        
        foreach (Renderer r in renderers)
            bounds.Encapsulate(r.bounds);

        Debug.Log("=== MODEL SIZE ===");
        Debug.Log("Width (X): " + bounds.size.x);
        Debug.Log("Height (Y): " + bounds.size.y);
        Debug.Log("Depth (Z): " + bounds.size.z);
    }
}
