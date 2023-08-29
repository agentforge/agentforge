(define (domain garden)

  (:requirements :strips :typing :negative-preconditions)

  (:types
    plant location strain - string
    seed clone - plant
    outdoor-plot indoor-pot - location
    plant-count - numeric
    water-container curing-container - container
    container tool amendment - boolean
    mulch fertilizer - amendment
  )

  (:predicates
    (prepared ?location - location)
    (flowering ?plant - plant)
    (watered-plant ?plant - plant)
    (mulched ?location - location)
    (fertilized ?location - location)
    (infested ?plant - plant)
    (weeds ?location - location)
    (dug ?location - location)
    (planted ?plant - plant ?location - location)
    (watered-plant ?plant - plant)
    (watered-location ?location - location)
    (matured ?plant - plant)
    (alive ?plant - plant)
    (growing ?plant - plant)
    (digging-tool-available ?digging-tool - tool)
    (fertilizer-available ?fertilizer - fertilizer)
    (growing-location-fertilized ?location - location)
    (mulch-available ?mulch - mulch)
    (water-container-available ?water-can - water-container)
    (indoor-pot-available ?indoor-pot - indoor-pot)
    (empty ?water-can - container)
    (dry ?location - location)
    (unplanted ?location - location)
    (germinating ?seed - seed)
    (plant-in-curing-container ?plant - plant ?curing-container - curing-container)
    (plant-drying ?plant - plant)
    (freezing-conditions ?outdoor-plot - outdoor-plot)
    (amendment-available ?amendment - amendment)
    (amended ?location - location)
    (seed-available ?seed - seed)
    (clone-available ?clone - clone)
    (strain-chosen ?plant)
    (outdoot-plot-available ?outdoor-plot - outdoor-plot)
  )

  (:action get-fertilizer
    :parameters (?fertilizer - fertilizer)
    :effect (fertilizer-available ?fertilizer))

  (:action get-digging-tool
    :parameters (?digging-tool - tool)
    :effect (digging-tool-available ?digging-tool))

  (:action prep-outdoor-plot
    :parameters (?outdoor-plot - outdoor-plot ?plant - plant)
    :effect (outdoot-plot-available ?outdoor-plot))

  (:action get-indoor-pots
    :parameters (?indoor-pot - indoor-pot ?plant - plant)
    :effect (indoor-pot-available ?indoor-pot))

  (:action get-seeds
    :parameters (?seed - seed ?plant - plant)
    :effect (seed-available ?seed))

  (:action choose-strain
    :parameters (?strain - strain)
    :effect (strain-chosen ?strain))

  (:action get-clone
    :parameters (?clone - clone ?plant - plant)
    :effect (clone-available ?clone))

  (:action prepare
    :parameters (?location - location ?digging-tool - tool ?plant-count - plant-count)
    :precondition (and (strain-chosen ?strain) (or (seed-available ?plant) (clone-available ?plant)) (or (outdoot-plot-available ?location) (indoor-pot-available ?location)) (digging-tool-available ?digging-tool) (fertilizer-available ?fertilizer))
    :effect (prepared ?location))

  (:action plant-it
    :parameters (?location - location ?plant - plant)
    :precondition (and (or (seed-available ?plant) (clone-available ?plant)) (prepared ?location))
    :effect (and (planted ?plant ?location) (growing ?plant)))

  (:action fill-watering-can
    :parameters (?water-can - container)
    :precondition (and (water-container-available ?water-can) (empty ?water-can))
    :effect (not (empty ?water-can)))

  (:action germinate
    :parameters (?location - location ?seed - seed)
    :precondition (prepared ?location)
    :effect (and (germinating ?seed)))

  (:action plant-germinated
    :parameters (?location - location ?plant - plant)
    :precondition (and (prepared ?location) (germinating ?plant))
    :effect (and (growing ?plant)))

  (:action sow
    :parameters (?location - location ?seed - seed)
    :precondition (and (dug ?location) (seed-available ?seed))
    :effect (and (growing ?seed) (planted ?seed ?location)))

  (:action sprout
    :parameters (?plant - plant ?location - location ?seed - seed)
    :precondition (planted ?seed ?location)
    :effect (and (growing ?plant ?location)))

  (:action transition-to-flowering
    :parameters (?plant - plant ?location - location)
    :precondition (and (growing ?plant) (alive ?plant))
    :effect (flowering ?plant))

  (:action harvest
    :parameters (?plant - plant ?location - location)
    :precondition (and (planted ?plant ?location) (flowering ?plant) (alive ?plant))
    :effect(and (not (planted ?plant ?location)) (not (alive ?plant)) (not (growing ?plant)) (harvested ?plant)))

  (:action dry-buds
    :parameters (?plant - plant ?curing-container - curing-container )
    :precondition (harvested ?plant)
    :effect(and (plant-drying ?plant) (plant-in-curing-container ?plant ?curing-container)))

  (:action water
    :parameters (?plant - plant ?water-can - water-container ?location - location)
    :precondition (and (alive ?plant) (water-container-available ?water-can) (not (empty ?water-can)))
    :effect (and (watered-plant ?plant) (not (dry ?location)) (empty ?water-can)))

  (:action apply-mulch
    :parameters (?location - location ?mulch - mulch)
    :precondition (and (dug ?location) (mulch-available ?mulch))
    :effect (mulched ?location))

  (:action dig-soil
    :parameters (?location - location ?digging-tool - tool)
    :precondition (and (prepared ?location) (not (dug ?location)) (digging-tool-available ?digging-tool))
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
    :parameters (?plant - plant ?pesticide - pesticide)
    :precondition (and (infested ?plant) (growing ?plant) (flowering ?plant) (alive ?plant) (pesticide-available ?pesticide))
    :effect (not (infested ?plant)))

  (:action prune
    :parameters (?plant - plant ?tool - tool)
    :precondition (and (flowering ?plant) (growing ?plant) (pruning-tool-available ?tool))
    :effect (pruned ?plant))

  (:action thin
    :parameters (?plant - plant)
    :precondition (growing ?plant)
    :effect (thinned ?plant))

  (:action train
    :parameters (?plant - plant)
    :precondition (growing ?plant)
    :effect (trained ?plant))

  (:action add-biocontrol
    :parameters (?plant - plant ?biocontrol - biocontrol)
    :precondition (and (growing ?plant) (infested ?location) (planted ?plant))
    :effect (not (infested ?location)))

  (:action remove-weeds
    :parameters (?outdoor-plot - outdoor-plot ?plant - plant)
    :precondition (and (weeds ?outdoor-plot) (growing ?plant) (planted ?plant ?outdoor-plot))
    :effect (not (weeds ?outdoor-plot)))

  (:action cover
    :parameters (?plant - plant ?outdoor-plot - outdoor-plot)
    :precondition (and (growing ?plant) (freezing-conditions ?outdoor-plot) (not (covered ?outdoor-plot)))
    :effect (covered ?outdoor-plot))

  (:action add-support-structure
    :parameters (?plant - plant ?structure - support-structure)
    :precondition (and (growing ?plant) (support-structure-available ?structure))
    :effect (supported ?plant))

  (:action pollinate
    :parameters (?plant - plant ?pollinator - pollinator)
    :precondition (and (growing ?plant) (flowering ?plant) (pollinator-available ?pollinator))
    :effect (pollinated ?plant))
)