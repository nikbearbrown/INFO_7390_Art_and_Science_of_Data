# Game Development Cheat Sheet

## Game Physics

### Physics Bodies
- **Rigidbody**: Responds to physics forces (gravity, collisions, etc.)
- **Kinematic Body**: Ignores external forces; must be moved manually
- **Static Body**: Cannot move; used for immovable scenery

### Collision Detection
- **Unity Requirements for OnCollisionEnter**:
  - At least one object must have a Rigidbody
  - Both objects must have a Collider component
  - Neither can have isTrigger enabled
- **Unity Requirements for OnTriggerEnter**:
  - At least one object must have a Rigidbody
  - Both must have Colliders
  - At least one must have isTrigger enabled
- **CompareTag()**: More efficient than direct string comparison (tag == "PickUp")

## Unity Basics

### MonoBehaviour Events
- **Start()**: Called once when the script is enabled, before any Update
- **Update()**: Called every frame
- **FixedUpdate()**: Called at a fixed time interval; use for physics calculations
- **LateUpdate()**: Called after all Updates; use for camera follow
- **Awake()**: Called when the script instance is being loaded
- **OnEnable()**: Called when the object becomes enabled and active
- **OnDisable()**: Called when the object becomes disabled or inactive

### Important Components
- **Transform**: Position, rotation, scale of GameObjects
- **Rigidbody**: Makes objects respond to the physics system
- **Collider**: Defines the shape for collision detection
- **Camera**: Renders the scene from its perspective
- **Renderer**: Makes objects visible (MeshRenderer, SpriteRenderer)
- **Animator**: Controls animations using animation controllers

## Unreal Engine Basics

### Blueprint Types
- **Level Blueprint**: Specific to one level; manages level-wide events
- **Class Blueprint**: Reusable objects that can be placed in multiple levels
- **Animation Blueprint**: Controls character animations

### Key Events
- **BeginPlay**: Runs once when the game starts or when the actor is spawned
- **Tick**: Runs every frame (like Update in Unity)
- **OnComponentBeginOverlap**: Called when this component begins overlapping another
- **OnComponentEndOverlap**: Called when this component stops overlapping another

### Casting
- Used to access specific properties and functions of a particular class
- Allows animation blueprints to interact with character-specific variables

## Shaders & Materials

### Key Material Properties
- **Albedo/Base Color**: The base color of the material without lighting
- **Metallic**: How metallic a surface is (reflective, conducts light)
- **Roughness**: How smooth or rough a surface is (affects reflection sharpness)
- **Normal**: Affects how light bounces off surfaces
- **Specular**: Controls direct reflection of light sources
- **Emission**: Makes materials appear to emit light

### Normals in 3D Rendering
- Vectors that define the direction a surface is facing
- Determine how light interacts with surfaces
- Critical for proper shading and lighting calculations

### UV Mapping
- Defines how 2D textures wrap around 3D models
- U and V coordinates correspond to X and Y in 2D texture space

## Particle Effects

### Particle System Components
- **Emitter**: Controls where and how particles are spawned
- **Lifetime**: How long particles exist
- **Size/Scale**: Controls particle dimensions
- **Color**: Can change over particle lifetime
- **Velocity/Direction**: Controls how particles move
- **Collision**: How particles interact with the environment

### Optimization Techniques
- **Particle Pooling**: Reuse particle instances instead of creating/destroying
- **LOD System**: Reduce detail for distant effects
- **Limit Overdraw**: Avoid having many transparent particles overlap
- **Use Flipbooks**: Animate textures rather than using many particles

## Animation

### Animation Types
- **Keyframe Animation**: Manually created poses at specific frames
- **Skeletal Animation**: Uses a hierarchical bone structure to control a mesh
- **Physics-Based Animation**: Simulates real-world physics for movement
- **Procedural Animation**: Generated through code rather than pre-created

### Animation Blending
- **Blend Trees**: Smoothly transition between animations based on parameters
- **Animation Layers**: Combine animations (e.g., upper body aiming while legs walking)
- **Additive Animations**: Add motion on top of base animations

### Animation Retargeting
- Allows animations created for one skeleton to be applied to different characters
- Preserves the essence of the animation while adjusting for differences in skeleton structure

## Audio

### Audio Components
- **Audio Source**: Emits sound from a location
- **Audio Listener**: Receives sounds (typically attached to the player camera)
- **Audio Mixer**: Organizes and adjusts audio channels and effects
- **Audio Effects**: Modify sounds (reverb, echo, distortion, etc.)

### Procedural Audio
- Dynamically generated sound based on in-game parameters
- Examples: Footsteps changing based on surface, adaptive music systems

## Profiling & Optimization

### Common Performance Bottlenecks
- **Draw Calls**: Too many separate objects being rendered
- **Polygon Count**: Too many triangles in view
- **Texture Size**: Overly high-resolution textures
- **Physics Calculations**: Too many rigidbodies or complex colliders
- **Script Performance**: Inefficient code execution

### Optimization Techniques
- **LOD (Level of Detail)**: Reduce model complexity at distance
- **Batching**: Combine draw calls to reduce rendering overhead
- **Object Pooling**: Reuse objects instead of instantiating/destroying them
- **Occlusion Culling**: Don't render objects that can't be seen
- **Texture Atlasing**: Combine multiple textures into one to reduce draw calls

## Game AI

### AI Architecture Types
- **Finite State Machines**: Simple states with transitions between them
- **Behavior Trees**: Hierarchical structure of tasks with priority
- **Utility AI**: Decision-making based on scoring potential actions
- **GOAP (Goal-Oriented Action Planning)**: AI that forms plans to achieve goals

### Common Enemy States
- **Patrol**: Moving along predetermined paths
- **Alert**: Aware of potential player presence
- **Chase**: Actively pursuing the player
- **Attack**: Engaging the player
- **Retreat**: Moving away from the player to safety
- **Searching**: Looking for a player that was previously detected

## C# Programming

### Memory Management
- **Stack**: Value types (int, float, bool, struct)
- **Heap**: Reference types (classes, arrays, strings)
- **new Operator**: Allocates memory on the heap
- **Garbage Collection**: Automatically frees memory that's no longer needed

### Static Variables/Methods
- Belong to the class itself, not any specific instance
- Shared among all instances of the class
- Can be accessed without creating an object of the class
- Use for data that should be consistent across all instances

### C# Best Practices in Unity
- Use [SerializeField] for inspector-visible private variables
- Prefer GetComponent<>() in Start/Awake rather than Update
- Use object pooling for frequently instantiated/destroyed objects
- Avoid FindObjectOfType() and GameObject.Find() in performance-critical code