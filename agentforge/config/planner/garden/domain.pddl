  (define (domain garden)

    (:requirements :strips :typing :negative-preconditions)

    (:types
      cannabis-plant location - string
      strain - cannabis-plant
      outdoor-plot indoor-pot - location
      water-container curing-container - container
      mulch fertilizer biocontrol pesticide - amendment
      container tool amendment support-structure - boolean
    )

    (:predicates
      (prepared ?location - location)
      (flowering ?cannabis-plant  - cannabis-plant)
      (mulched ?location - location)
      (fertilized ?location - location)
      (infested ?cannabis-plant  - cannabis-plant)
      (weeds ?location - location)
      (dug ?location - location)
      (planted ?cannabis-plant  - cannabis-plant ?location - location)
      (watered-plant ?cannabis-plant  - cannabis-plant)
      (watered-location ?location - location)
      (matured ?cannabis-plant  - cannabis-plant)
      (alive ?cannabis-plant  - cannabis-plant)
      (growing ?cannabis-plant  - cannabis-plant)
      (has-shovel-available ?digging-tool - tool)
      (fertilizer-available ?fertilizer - fertilizer)
      (growing-location-fertilized ?location - location)
      (mulch-available ?mulch - mulch)
      (water-container-available ?water-can - water-container)
      (has-indoor-pot-available ?location - location)
      (empty ?water-can - water-container)
      (dry ?location - location)
      (unplanted ?location - location)
      (germinating ?cannabis-plant - cannabis-plant)
      (plant-in-curing-container ?cannabis-plant  - cannabis-plant ?curing-container - curing-container)
      (plant-drying ?cannabis-plant  - cannabis-plant)
      (freezing-conditions ?outdoor-plot - outdoor-plot)
      (amendment-available ?amendment - amendment)
      (amended ?location - location)
      (has-seeds ?cannabis-plant - cannabis-plant)
      (has-clones ?cannabis-plant - cannabis-plant)
      (choose-strain ?strain - strain)
      (topped ?cannabis-plant - cannabis-plant ?location - location)
      (has-outdoor-plot-available ?location - location)
      (harvested ?cannabis-plant - cannabis-plant)
      (pesticide-available ?pesticide - pesticide)
      (pruning-tool-available ?pruning-tool - tool)
      (pruned ?cannabis-plant - cannabis-plant)
      (thinned ?cannabis-plant - cannabis-plant)
      (trained ?cannabis-plant - cannabis-plant)
      (covered ?outdoor-plot - outdoor-plot)
      (support-structure-available ?structure)
      (supported ?cannabis-plant - cannabis-plant)
      (watering-scheduled ?cannabis-plant - cannabis-plant)
      (fertilizer-scheduled ?cannabis-plant - cannabis-plant)
      (pest-control-scheduled ?cannabis-plant - cannabis-plant)
      (thinning-scheduled ?cannabis-plant - cannabis-plant)
      (training-scheduled ?cannabis-plant - cannabis-plant)
      (topping-scheduled ?cannabis-plant - cannabis-plant)
      (has-photoperiod-genetics ?cannabis-plant - cannabis-plant)
      (has-autoflower-genetics ?cannabis-plant - cannabis-plant)
    )

    (:action prepare
      :parameters (?location - location ?digging-tool - tool ?cannabis-plant - cannabis-plant ?strain - strain ?fertilizer - fertilizer)
      :precondition (and (choose-strain ?strain) (or (has-seeds ?cannabis-plant) (has-clones ?cannabis-plant)) (or (has-outdoor-plot-available ?location) (has-indoor-pot-available ?location)) (or (has-autoflower-genetics ?cannabis-plant) (has-photoperiod-genetics ?cannabis-plant)) (has-shovel-available ?digging-tool) (fertilizer-available ?fertilizer))
      :effect (prepared ?location))

    (:action plant-it
      :parameters (?location - location ?cannabis-plant - cannabis-plant)
      :precondition (and (has-clones ?cannabis-plant) (prepared ?location))
      :effect (and (planted ?cannabis-plant ?location) (growing ?cannabis-plant)))

    (:action fill-watering-can
      :parameters (?water-can - water-container)
      :precondition (and (water-container-available ?water-can) (empty ?water-can))
      :effect (not (empty ?water-can)))

    (:action germinate
      :parameters (?location - location ?cannabis-plant - cannabis-plant)
      :precondition (prepared ?location)
      :effect (and (germinating ?cannabis-plant)))

    (:action plant-germinated
      :parameters (?location - location ?cannabis-plant  - cannabis-plant)
      :precondition (and (prepared ?location) (germinating ?cannabis-plant))
      :effect (and (growing ?cannabis-plant)))

    (:action sow
      :parameters (?location - location ?cannabis-plant - cannabis-plant)
      :precondition (and (dug ?location) (has-seeds ?cannabis-plant))
      :effect (and (planted ?cannabis-plant ?location)))

    (:action sprout
      :parameters (?cannabis-plant  - cannabis-plant ?location - location)
      :precondition (planted ?cannabis-plant ?location)
      :effect (and (growing ?cannabis-plant)))

    (:action top
      :parameters (?cannabis-plant  - cannabis-plant ?location - location)
      :precondition (growing ?cannabis-plant)
      :effect (topped ?cannabis-plant ?location))

    (:action transition-to-flowering
      :parameters (?cannabis-plant  - cannabis-plant ?location - location)
      :precondition (and (growing ?cannabis-plant) (planted ?cannabis-plant ?location) (matured ?cannabis-plant))
      :effect (flowering ?cannabis-plant))

    (:action harvest
      :parameters (?cannabis-plant  - cannabis-plant ?location - location)
      :precondition (and (planted ?cannabis-plant ?location) (flowering ?cannabis-plant) (alive ?cannabis-plant))
      :effect(and (not (planted ?cannabis-plant ?location)) (not (alive ?cannabis-plant)) (not (growing ?cannabis-plant)) (harvested ?cannabis-plant)))

    (:action dry-buds
      :parameters (?cannabis-plant  - cannabis-plant ?curing-container - curing-container )
      :precondition (harvested ?cannabis-plant)
      :effect(and (plant-drying ?cannabis-plant) (plant-in-curing-container ?cannabis-plant ?curing-container)))

    (:action water
      :parameters (?cannabis-plant  - cannabis-plant ?water-can - water-container ?location - location)
      :precondition (and (alive ?cannabis-plant) (water-container-available ?water-can) (not (empty ?water-can)))
      :effect (and (watered-plant ?cannabis-plant) (not (dry ?location)) (empty ?water-can)))

    (:action apply-mulch
      :parameters (?location - location ?mulch - mulch)
      :precondition (and (dug ?location) (mulch-available ?mulch))
      :effect (mulched ?location))

    (:action dig-soil
      :parameters (?location - location ?digging-tool - tool)
      :precondition (and (prepared ?location) (has-shovel-available ?digging-tool))
      :effect (dug ?location))

    (:action amend-soil
      :parameters (?location - location ?amendment - amendment)
      :precondition (and (prepared ?location) (amendment-available ?amendment))
      :effect (amended ?location))

    (:action apply-fertilizer
      :parameters (?location - location ?fertilizer - fertilizer)
      :precondition (and (fertilizer-available ?fertilizer))
      :effect (fertilized ?location))

    (:action apply-pesticide
      :parameters (?cannabis-plant  - cannabis-plant ?pesticide - pesticide)
      :precondition (and (infested ?cannabis-plant) (growing ?cannabis-plant) (flowering ?cannabis-plant) (alive ?cannabis-plant) (pesticide-available ?pesticide))
      :effect (not (infested ?cannabis-plant)))

    (:action prune
      :parameters (?cannabis-plant  - cannabis-plant ?pruning-tool - tool)
      :precondition (and (flowering ?cannabis-plant) (growing ?cannabis-plant) (pruning-tool-available ?pruning-tool))
      :effect (pruned ?cannabis-plant))

    (:action thin
      :parameters (?cannabis-plant  - cannabis-plant)
      :precondition (growing ?cannabis-plant)
      :effect (thinned ?cannabis-plant))

    (:action train
      :parameters (?cannabis-plant  - cannabis-plant)
      :precondition (growing ?cannabis-plant)
      :effect (trained ?cannabis-plant))

    (:action add-biocontrol
      :parameters (?cannabis-plant  - cannabis-plant ?biocontrol - biocontrol ?location - location)
      :precondition (and (growing ?cannabis-plant) (infested ?cannabis-plant) (planted ?cannabis-plant ?location))
      :effect (not (infested ?cannabis-plant)))

    (:action remove-weeds
      :parameters (?outdoor-plot - outdoor-plot ?cannabis-plant  - cannabis-plant)
      :precondition (and (weeds ?outdoor-plot) (growing ?cannabis-plant) (planted ?cannabis-plant ?outdoor-plot))
      :effect (not (weeds ?outdoor-plot)))

    (:action cover
      :parameters (?cannabis-plant  - cannabis-plant ?outdoor-plot - outdoor-plot)
      :precondition (and (growing ?cannabis-plant) (freezing-conditions ?outdoor-plot) (not (covered ?outdoor-plot)))
      :effect (covered ?outdoor-plot))

    (:action add-support-structure
      :parameters (?cannabis-plant  - cannabis-plant ?structure - support-structure)
      :precondition (and (growing ?cannabis-plant) (support-structure-available ?structure))
      :effect (supported ?cannabis-plant))
  )