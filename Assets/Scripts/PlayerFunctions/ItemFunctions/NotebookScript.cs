using UnityEngine;

public class NotebookScript : MonoBehaviour
{
	private void Start()
	{
		up = true;
	}
	private void Update()
	{
		if (gc.mode == "endless")
		{
			if (respawnTime > 0f)
			{
				if ((transform.position - player.position).magnitude > 60f)
				{
					respawnTime -= Time.deltaTime;
				}
			}
			else if (!up)
			{
				transform.position = new Vector3(transform.position.x, 4f, transform.position.z);
				up = true;
				audioDevice.Play();
			}
		}
		if (Singleton<InputManager>.Instance.GetActionKey(InputAction.Interact) && Time.timeScale != 0f)
		{
			Ray ray = Camera.main.ScreenPointToRay(new Vector3((float)(Screen.width / 2), (float)(Screen.height / 2), 0f));
			RaycastHit raycastHit;
			if (Physics.Raycast(ray, out raycastHit) && (raycastHit.transform.tag == "Notebook" & Vector3.Distance(player.position, transform.position) < openingDistance))
			{
				transform.position = new Vector3(transform.position.x, -20f, transform.position.z);
				up = false;
				respawnTime = 120f;
				gc.CollectNotebook();
				// [MOD] TEMPLATE: Show the hit text and play the hit sound instead of the math minigame.
				gc.ShowHitText();
				// [MOD] TEMPLATE: Baldi gets angry from the 2nd notebook on.
				if (gc.notebooks >= 2)
				{
					gc.GetAngry(1f);
				}
			}
		}
	}
	public float openingDistance;
	public GameControllerScript gc;
	public BaldiScript bsc;
	public float respawnTime;
	public bool up;
	public Transform player;
	public GameObject learningGame;
	public AudioSource audioDevice;
}
