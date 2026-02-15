# heightfield_erode-2.0 (SOP)

## Intent

Simulates realistic terrain erosion via hydraulic (water-based) and thermal (freeze-thaw) processes over time. This is version 2.0, used before the complete rewrite in Houdini 21.

## Core Behavior

- **Simulation node**: Requires playback/animation to see effects (appears inactive on frame 1)
- **Multi-layer output**: Generates `height`, `debris`, `sediment`, `water`, `bedrock`, `mask`, `flow`, `flowdir` volume layers
- **Frame-iterative**: Each frame builds on the previous frame's state
- **Volume topology stable**: Points/prims count remains constant (6 prims for 6 layers); erosion changes voxel values inside volumes

## Key Parameters

### Main Tab

**Hydro (Hydraulic Erosion)**:
- `erodability`: Controls softness of material (higher = easier erosion, deeper channels)
- `erosionrate`: Multiplier on erodability
- `bankangle`: Riverbank slope angle (lower = wider/flatter channels, higher = narrow/deep channels)
- `water_spreaditers`: Iterations of water spreading (more = longer, less dense incisions)

**Thermal (Freeze-Thaw Erosion)**:
- `thermal_erodability`: Softness for thermal weathering
- `cutangle`: Angle where thermal erosion stops (lower = flatter cuts, more erosion)

### Advanced Tab

**Hydro Erosion**:
- `hydro_removalrate`: Proportion of debris deleted (simulates water carrying debris away; 0=no deletion, negative=debris less dense than rock)
- `hydro_maxdebrisdepth`: Stop erosion when debris reaches this depth
- `hydro_gridbias`: Movement bias direction (positive=principal axes, negative=45° angles, 0=no bias)

**Erodability**:
- `hydro_erodability_rampupiters`: Iteration where erodability reaches maximum
- `hydro_erodability_initialfactor`: Initial erodability fraction
- `hydro_erodability_slopefactor`: Slope influence on erosion (higher=more slope effect)

**Riverbed**:
- `hydro_bed_erosionratefactor`: Multiplier for riverbed-only erosion (increases incision depth)
- `hydro_bed_depositionrate`: Rate sediment converts to debris (0=no conversion, 1=all sediment becomes debris, protecting bedrock)
- `hydro_bed_sedimentcap`: Sediment capacity per unit of moving water (higher=longer erosion before deposition)

**Riverbank**:
- `hydro_bank_erosionratefactor`: Multiplier for riverbank-only erosion (increases channel width)
- `hydro_bank_maxbankbedwaterratio`: Max bank-to-bed water column height ratio considered as riverbank

**Thermal Erosion**:
- `thermal_removalrate`: Proportion of thermal debris deleted (wind carrying debris away)
- `thermal_maxdebrisdepth`: Stop thermal erosion at this debris depth

**Precipitation**:
- `maskpreciplayer`: Mask layer name controlling rainfall distribution
- `rain_amount`: Rainfall per frame (very large values create underwater terrain)
- `rain_density`: Raindrop packing (smaller=more erosion lines, larger=wider/sparser cracks)
- `rain_evaporation`: Evaporation rate (higher=less pooled water)

**Raindrop Settings**:
- `rain_expandradius`: Raindrop radius expansion (larger drops = sparser/wider incisions)
- `rain_blurradius`: Water column blur radius (increases incision width and smoothness)

**Water Flow**:
- `water_quant`: Water flow chunkiness (lower=continuous, higher=chunky)
- `water_postsmooth`: Smooth water as post-process

**Debris Flow**:
- `debris_iterations`: Spread algorithm iterations per frame
- `debris_quant`: Debris flow chunkiness
- `debris_postsmooth`: Smooth debris as post-process
- `water_absor`: Debris movement based on flow field (higher=stops near channels, lower=ignores channels)
- `debris_maxheight`: Max wet debris height before movement resumes
- `debris_repose`: Repose angle in degrees (max slope for stable debris; lower=less pile-up like sand, higher=more pile-up like rocks)

### Bedrock Tab

**Bedrock Override**: Replace bedrock layer each frame from second input
**Adjust Height by Bedrock Change**: Add net new bedrock height while erosion occurs (enables mountain-building animation)

**Strata**:
- `Adjust Erodability by Strata`: Vary erodability by depth from reference bedrock
- `Strata Depth`: Depth range for strata (positive=below bedrock, negative=above bedrock)
- `Clamp at Strata Bounds`: Clamp or repeat pattern outside strata range
- `Strata Erodability`: Ramp defining erodability at different strata depths (1=fully erodable like dirt, 0=prevents erosion like granite)

### Layers Tab

- `debris_removefromheight`: Keep input debris layer but exclude from erosion calculations
- `water_removefromheight`: Keep input water layer but exclude from erosion calculations
- `clearwater`, `cleardebris`, `clearsediment`: Reset respective layers
- `debris_addtoheight`: Add debris layer values to final height (default on)
- `water_addtoheight`: Add water elevation to final height (default off; useful for "baking" water into flat terrain)

## Typical Workflow

### Basic Erosion

```
heightfield -> heightfield_noise -> heightfield_erode::2.0 -> OUT
```

- Start simulation at frame 1
- Play to desired frame (e.g., frame 20-50)
- Once converged, use `Freeze` parameter or export via `heightfield_output`

### Multi-Resolution Upscaling

Pattern from official `upscaling` example:

```
heightfield (gridspacing=4) -> noise -> distort -> noise
  -> heightfield_erode::2.0 (low-res pass)
  -> timeshift (freeze at frame 5)
  -> heightfield_resample (resscale=2.0)
  -> heightfield_erode::2.0 (mid-res pass)
  -> timeshift (freeze at frame 5)
  -> heightfield_resample (resscale=2.0)
  -> heightfield_erode::2.0 (final-res pass)
```

**Key insight**: Start erosion at low resolution (large `gridspacing`), freeze result at convergence frame, double resolution, continue erosion. Repeat for final resolution. Each pass refines detail without recomputing full high-res simulation from scratch.

### Custom Solver-Based Erosion

Pattern from official `volcano` example:

- Use `solver` SOP with custom internal logic
- Create separate fluid layers (e.g., `lava`, `water`) via `heightfield_copylayer` + `volumewrangle`
- Use masks to control where each fluid type precipitates
- Implement custom interaction rules (e.g., lava + water = solidified rock added to height)
- Use negative `Amount` on flow nodes to reverse erosion (mass buildup instead of removal)

## Production Usage

### First-Pass Erosion Settings (from docs)

On __Advanced__ tab:

- Under __Hydro > Erodability Adjustments__:
  - Set `hydro_erodability_rampupiters` to `0`
  - Set `hydro_erodability_initialfactor` to `1`
  - Set `hydro_erodability_slopefactor` to `0`

- Under __Hydro > Riverbed__:
  - Set `hydro_bed_sedimentcap` to `20`

- Under __Debris flow__:
  - Turn `debris_postsmooth` on

### Controlling Look

**Channel shape**:
- Wide/shallow channels: Lower `hydro_bankangle`, increase `rain_density`, increase `rain_expandradius`, increase `rain_blurradius`
- Narrow/deep channels: Increase `hydro_bankangle`, decrease `rain_density`, decrease `rain_expandradius`, decrease `rain_blurradius`

**Ridge shape**:
- Sharp ridges: Lower `thermal_cutangle`
- Rounded ridges: Increase `thermal_cutangle`

**Lakes**:
- Big lakes: Lower `rain_evaporation`
- Small/no lakes: Increase `rain_evaporation`
- Harsh lake edges: Lower `rain_blurradius`
- Smooth lake edges: Increase `rain_blurradius`

**Debris**:
- Smooth debris flow: Lower `debris_quant`
- Grainy debris flow: Increase `debris_quant`
- Less debris on ridges: Lower `debris_maxheight`
- More debris on ridges: Increase `debris_maxheight`
- Sand-like pile-up: Lower `debris_repose`
- Rock-like pile-up: Increase `debris_repose`

### Gotchas

- **Frame 1 appears inactive**: Erosion is iterative; must play animation to see effects
- **Pitting/holes**: Reduce `hydro_maxdebrisdepth` or `thermal_maxdebrisdepth`
- **Uneven erosion**: Use masked `gridbias` remapped to range `-1` to `1`
- **Negative removal rates**: Valid; simulates debris being less dense than rock (one unit eroded rock produces >1 unit debris)
- **Reset Simulation button**: Ctrl-Click to reset to start frame; clicking on high frame numbers forces re-simulation of all prior frames (slow)
- **Freeze behavior**: Use `Freeze` toggle and `Freeze at Frame` to lock output once desired frame is determined

## Companion Nodes

- `heightfield`: Base flat heightfield generator
- `heightfield_noise`: Add initial terrain variation before erosion
- `heightfield_distort`: Warp heightfield for more organic shapes
- `heightfield_resample`: Change resolution (used in multi-res upscaling workflows)
- `timeshift`: Freeze simulation at specific frame before upscaling
- `heightfield_copylayer`: Duplicate or create custom layers
- `volumewrangle`: Custom layer manipulation (masks, fluid interactions)
- `heightfield_output`: Export final terrain to disk
- `heightfield_visualize`: Visualize elevation ramps and layer colors (erosion node has built-in visualization on __Visualization__ tab)
- `solver`: Custom erosion logic with per-frame control

## Version Notes

- This is version 2.0 (since Houdini 17.0)
- Houdini 21.0 introduced version 3.0 with complete rewrite (faster, easier to use)
- Version 2.0 still available for legacy setups
- Doc file path: `nodes/sop/heightfield_erode-2.0.txt` (note hyphen, not underscore in version suffix)

## Related Nodes

- `heightfield_erode` (v3.0): Rewritten version in H21+
- `heightfield_erode_hydro`: Simulates erosion from one heightfield source to another
- `heightfield_slump`: Non-iterative erosion (calculates and applies effect at once)
- `heightfield_flowfield`: Generate flow field without erosion simulation

## Study Validation

- ✅ Read official docs: `nodes/sop/heightfield_erode-2.0.txt`
- ✅ Reviewed examples: `upscaling`, `volcano`
- ✅ Inspected example networks: Multi-res upscaling pattern, custom solver-based erosion
- ✅ Read sticky notes: Upscaling workflow, custom lava/water interaction rules
- ✅ Live validation network: `/obj/academy_heightfield_erode_live`
- ✅ Parameter testing: `hydro_erosionrate`, `hydro_bankangle`, `rain_amount` (volume topology stable, voxel values change)
- ✅ Multi-frame probe: Verified layer generation at frames 1, 10, 20
