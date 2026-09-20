using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
	private void Awake()
	{
		mouseSensitivity = PlayerPrefs.GetFloat("MouseSensitivity", 200f);
	}
	private void Start()
	{
		stamina = staminaMax;
		Time.timeScale = 1f;
	}
	private void Update()
	{
		running = Singleton<InputManager>.Instance.GetActionKey(InputAction.Run);
		MouseMove();
		PlayerMove();
		StaminaUpdate();
	}
	private void MouseMove()
	{
		Quaternion rotation = transform.rotation;
		rotation.eulerAngles += new Vector3(0f, Singleton<InputManager>.Instance.GetLookAxisX() * mouseSensitivity * Time.deltaTime * Time.timeScale, 0f);
		transform.rotation = rotation;
	}
	private void PlayerMove()
	{
		float d = walkSpeed;
		if (stamina > 0f & running)
		{
			d = runSpeed;
		}
		Vector2 moveAxis = Singleton<InputManager>.Instance.GetMoveAxis();
		Vector3 a = transform.right * moveAxis.x;
		Vector3 b = transform.forward * moveAxis.y;
		sensitivity = Mathf.Clamp((a + b).magnitude, 0f, 1f);
		cc.Move((a + b).normalized * d * sensitivity * Time.deltaTime);
	}
	public void StaminaUpdate()
	{
		if (cc.velocity.magnitude > cc.minMoveDistance)
		{
			if (running)
			{
				stamina = Mathf.Max(stamina - staminaDrop * Time.deltaTime, 0f);
			}
		}
		else if (stamina < staminaMax)
		{
			stamina += staminaRise * Time.deltaTime;
		}
	}
	public CharacterController cc;
	public float walkSpeed;
	public float runSpeed;
	public float stamina;
	public float staminaDrop;
	public float staminaRise;
	public float staminaMax;
	private float sensitivity;
	private float mouseSensitivity;
	private bool running;
}
