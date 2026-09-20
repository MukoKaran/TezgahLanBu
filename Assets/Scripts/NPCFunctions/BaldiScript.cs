using UnityEngine;
using UnityEngine.AI;

public class BaldiScript : MonoBehaviour
{
	private void Start()
	{
		baldiAudio = GetComponent<AudioSource>(); //Get The Baldi Audio Source(Used mostly for the slap sound)
		agent = GetComponent<NavMeshAgent>(); //Get the Nav Mesh Agent
		if (agent == null)
		{
			agent = gameObject.AddComponent<NavMeshAgent>();
			agent.speed = speed > 0f ? speed : 150f;
			agent.angularSpeed = 120f;
			agent.acceleration = 500f;
		}
		if (navMeshBaseOffset != 0f) agent.baseOffset = navMeshBaseOffset;
		timeToMove = baseTime; //Sets timeToMove to baseTime
		Wander(); //Start wandering
		if (PlayerPrefs.GetInt("Rumble") == 1)
		{
			rumble = true;
		}
		// [MOD] Baldi's speed (ruler interval unchanged). Only if not set before.
		if (baseSpeed <= 0f)
		{
			baseSpeed = 150f;
			speed = baseSpeed;
		}
		baldiSpeedScale = 6f;
		// [MOD] Speed Baldi: gets faster over time (in all modes). +5 speed every 10 seconds.
		speedRampTimer = 0f;
		// [MOD] Load the clip used for the approaching sound.
		chaseLoop = Resources.Load<AudioClip>("Sound/BAL_Hi");
		if (slap == null)
		{
			slap = Resources.Load<AudioClip>("Sound/BAL_Slap");
		}
	}
	private void Update()
	{
		if (timeToMove > 0f) //If timeToMove is greater then 0, decrease it
		{
			timeToMove -= 1f * Time.deltaTime;
		}
		else
		{
			Move(); //Start moving
		}
		if (coolDown > 0f) //If coolDown is greater then 0, decrease it
		{
			coolDown -= 1f * Time.deltaTime;
		}
		if (baldiTempAnger > 0f) //Slowly decrease Baldi's temporary anger over time.
		{
			baldiTempAnger -= 0.02f * Time.deltaTime;
		}
		else
		{
			baldiTempAnger = 0f; //Cap its lowest value at 0
		}
		if (antiHearingTime > 0f) //Decrease antiHearingTime, then when it runs out stop the effects of the antiHearing tape
		{
			antiHearingTime -= Time.deltaTime;
		}
		else
		{
			antiHearing = false;
		}
		if (endless) //Only activate if the player is playing on endless mode
		{
			if (timeToAnger > 0f) //Decrease the timeToAnger
			{
				timeToAnger -= 1f * Time.deltaTime;
			}
			else
			{
				timeToAnger = angerFrequency; //Set timeToAnger to angerFrequency
				GetAngry(angerRate); //Get angry based on angerRate
				angerRate += angerRateRate; //Increase angerRate for next time
			}
		}
		// [MOD] Speed Baldi: gets faster over time (in all modes). +5 baseSpeed every 10 seconds.
		speedRampTimer += Time.deltaTime;
		if (speedRampTimer >= 10f)
		{
			speedRampTimer = 0f;
			baseSpeed += 5f;
			speed = baseSpeed;
		}
		// [MOD] Continuous warning sound when getting close (fix for Baldi approaching silently).
		if (player != null)
		{
			float dist = Vector3.Distance(transform.position, player.position);
			if (dist < 40f)
			{
				if (!baldiAudio.isPlaying)
				{
					// [MOD] BAL_Hi chase loop removed; only the slap sound plays.
				}
				else
				{
					baldiAudio.volume = Mathf.Clamp(1f - dist / 40f, 0.1f, 1f);
				}
			}
			else if (baldiAudio.isPlaying)
			{
				baldiAudio.Stop();
			}
		}
	}
	private void FixedUpdate()
	{
		if (freezeTimer > 0f) // [MOD] If frozen, don't move at all.
		{
			freezeTimer -= Time.fixedDeltaTime;
			agent.speed = 0f;
			return;
		}
		if (stunTimer > 0f) // [MOD] Sersemletildiysa dur (cetvel sesi de kesilsin).
		{
			stunTimer -= Time.fixedDeltaTime;
			agent.speed = 0f;
			if (baldiAudio.isPlaying) baldiAudio.Stop();
			return;
		}
		if (moveFrames > 0f) //Move for a certain amount of frames, and then stop moving.(Ruler slapping)
		{
			moveFrames -= 1f;
			float currentSpeed = speed;
			if (slowTimer > 0f) // [MOD] BSODA slow-down.
			{
				slowTimer -= Time.fixedDeltaTime;
				agent.speed = currentSpeed * slowMultiplier;
			}
			else
			{
				agent.speed = currentSpeed;
			}
		}
		else
		{
			agent.speed = 0f;
		}
		Vector3 direction = player.position - transform.position; 
		RaycastHit raycastHit;
		// [MOD] Use short-circuit && so that when the ray hits nothing, raycastHit.transform is not accessed (avoids NullReferenceException).
		if (Physics.Raycast(transform.position + Vector3.up * 2f, direction, out raycastHit, float.PositiveInfinity, 769, QueryTriggerInteraction.Ignore) && raycastHit.transform != null && raycastHit.transform.tag == "Player") //Create a raycast, if the raycast hits the player, Baldi can see the player
		{
			db = true;
			TargetPlayer(); //Start attacking the player
		}
		else
		{
			db = false;
		}
	}
	private void Wander()
	{
		if (wanderer != null && wanderTarget != null)
		{
			wanderer.GetNewTarget();
			agent.SetDestination(wanderTarget.position);
		}
		else if (player != null)
		{
			agent.SetDestination(player.position);
		}
		coolDown = 1f;
		currentPriority = 0f;
	}
	public void TargetPlayer()
	{
		agent.SetDestination(player.position); //Target the player
		coolDown = 1f;
		currentPriority = 0f;
	}
	private void Move()
	{
		if (transform.position == previous & coolDown < 0f) // If Baldi reached his destination, start wandering
		{
			Wander();
		}
		moveFrames = 1f; // [MOD] Near-instant ruler slap (about 10ms).
		timeToMove = baldiWait - baldiTempAnger;
		previous = transform.position; // Set previous to Baldi's current location
		// [MOD] Sound changes with distance (close = loud, far = quiet).
		float dist = Vector3.Distance(transform.position, player.position);
		float vol = Mathf.Clamp(1f - dist / 60f, 0.05f, 1f);
		float pitch = Mathf.Clamp(1.4f - dist * 0.01f, 0.6f, 1.4f);
		baldiAudio.volume = vol;
		baldiAudio.pitch = pitch;
		baldiAudio.PlayOneShot(slap); //Play the slap sound
		// [MOD] Play the "ADAMA 8 VURDUM" sound separately.
		if (adamaVurdum != null) baldiAudio.PlayOneShot(adamaVurdum);
		if (baldiAnimator != null) // [MOD] Don't error out if there is no animator/controller.
		{
			try
			{
				baldiAnimator.SetTrigger("slap"); // Play the slap animation
			}
			catch (System.Exception)
			{
				// No AnimatorController assigned, skip silently.
			}
		}
		if (rumble)
		{
			float num = Vector3.Distance(transform.position, player.position);
			if (num < vibrationDistance)
			{
				float motorLevel = 1f - num / vibrationDistance;
			}
		}
	}
	public void GetAngry(float value)
	{
		baldiAnger += value; // Increase Baldi's anger by the value provided
		if (baldiAnger < 0.5f) //Cap Baldi anger at a minimum of 0.5
		{
			baldiAnger = 0.5f;
		}
		// [MOD] Notebook-count based speed-up removed; constant fast slapping instead.
		baldiWait = 0.001f;
	}
	public void GetTempAngry(float value)
	{
		baldiTempAnger += value; //Increase Baldi's Temporary Anger
	}
	public void Hear(Vector3 soundLocation, float priority)
	{
		if (!antiHearing && priority >= currentPriority) //If anti-hearing is not active and the priority is greater then the priority of the current sound
		{
			agent.SetDestination(soundLocation); //Go to that sound
			currentPriority = priority; //Set the current priority to the priority
		}
	}
	public void ActivateAntiHearing(float t)
	{
		Wander(); //Start wandering
		antiHearing = true; //Set the antihearing variable to true for other scripts
		antiHearingTime = t; //Set the time the tape's effect on baldi will last
	}
	public bool db;
	public float baseTime;
	public float speed;
	public float timeToMove;
	public float baldiAnger;
	public float baldiTempAnger;
	public float baldiWait;
	public float baldiSpeedScale;
	private float moveFrames;
	private float currentPriority;
	public bool antiHearing;
	public float antiHearingTime;
	public float vibrationDistance;
	public float angerRate;
	public float angerRateRate;
	public float angerFrequency;
	public float timeToAnger;
	public bool endless;
	public Transform player;
	public Transform wanderTarget;
	public AILocationSelectorScript wanderer;
	private AudioSource baldiAudio;
	public AudioClip slap;
	public AudioClip adamaVurdum;
	public Animator baldiAnimator;
	public float coolDown;
	private Vector3 previous;
	private bool rumble;
	public NavMeshAgent agent;
	public float navMeshBaseOffset = 0f;
	// [MOD] BSODA slow-down.
	public float baseSpeed;
	private float slowTimer;
	private float slowMultiplier = 0.3f;
	public void ApplySlow(float duration)
	{
		slowTimer = duration;
	}
	// [MOD] Freeze Baldi.
	private float freezeTimer = 0f;
	public void ApplyFreeze(float duration)
	{
		freezeTimer = duration;
	}
	// [MOD] Stun Baldi: he stops, the ruler sound cuts off, then he continues.
	private float stunTimer = 0f;
	public void ApplyStun(float duration)
	{
		stunTimer = duration;
	}
	// [MOD] Speed Baldi: timer for getting faster over time.
	private float speedRampTimer = 0f;
	// [MOD] Approaching sound.
	private AudioClip chaseLoop;
	// [MOD] Difficulty increase (when Hardcore BSODA isn't used).
	public void IncreaseDifficulty(float amount)
	{
		baseSpeed += amount;
		speed = baseSpeed;
	}
}
