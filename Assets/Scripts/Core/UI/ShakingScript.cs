using UnityEngine;

[ExecuteAlways]
public class ShakingScript : MonoBehaviour
{
	private RectTransform rectTransform;

	private Vector2 initialPosition;

	public float Intensity = 5f;

	private void OnEnable()
	{
		rectTransform = GetComponent<RectTransform>();
		if (rectTransform == null)
		{
			Debug.LogWarning("ShakingScript requires a RectTransform!");
			return;
		}
		initialPosition = rectTransform.anchoredPosition;
	}

	private void OnDisable()
	{
		if (rectTransform != null)
		{
			rectTransform.anchoredPosition = initialPosition;
		}
	}

	private void Update()
	{
		if (Application.isPlaying)
		{
			Shake();
		}
	}

	private void Shake()
	{
		if (!(rectTransform == null))
		{
			rectTransform.anchoredPosition = initialPosition + new Vector2(Random.Range(0f - Intensity, Intensity), Random.Range(0f - Intensity, Intensity));
		}
	}
}
