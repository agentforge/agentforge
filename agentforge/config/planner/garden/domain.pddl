(define (domain garden)

  (:requirements :strips :typing :negative-preconditions)

  (:types
    plant - string
    seed clone - plant
    plot pot - location
    location - numeric
    water-container curing-container - container
    container tool amendment - boolean
    mulch fertilizer - amendment
  )

  (:predicates
    (prepared ?location - location)
    (flowering ?plant - plant)
    (watered-plant ?plant - plant)
    (mulched ?plot - plot)
    (fertilized ?location - location)
    (infested ?plant - plant)
    (weeds ?plot - plot)
    (dug ?location - location)
    (planted ?plant - plant ?location - location)
    (watered-plant ?plant - plant)
    (watered-plot ?plot - plot)
    (matured ?plant - plant)
    (alive ?plant - plant)
    (growing ?plant - plant)
    (digging-tool-available ?digging-tool - tool)
    (seed-available ?seed - seed)
    (clone-available ?clone - clone)
    (fertilizer-available ?fertilizer - fertilizer)
    (growing-location-fertilized ?location - location)
    (mulch-available ?mulch - mulch)
    (water-container-available ?water-can - water-container)
    (pot-available ?pot - pot)
    (empty ?water-can - container)
    (dry ?plot - plot)
    (unplanted ?location - location)
    (germinating ?seed - seed)
    (plant-in-curing-container ?plant - plant ?curing-container - curing-container)
    (plant-drying ?plant - plant)
    (freezing-conditions ?plot - plot)
    (amendment-available ?amendment - amendment)
    (amended ?location - location)
    (plant-available ?plant - plant)
  )

  (:action get-fertilizer
    :parameters (?fertilizer - fertilizer)
    :effect (fertilizer-available ?fertilizer))

  (:action get-digging-tool
    :parameters (?digging-tool - tool)
    :effect (digging-tool-available ?digging-tool))

  (:action get-pots
    :parameters (?pot - pot ?plant - plant)
    :effect (pot-available ?pot))

  (:action get-seeds
    :parameters (?seed - seed)
    :effect (plant-available ?seed))

  (:action get-clone
    :parameters (?clone - clone)
    :effect (plant-available ?clone))

  (:action prepare
    :parameters (?location - location ?digging-tool - tool)
    :precondition (and (digging-tool-available ?digging-tool) (unplanted ?pot) (dry ?pot) (fertilized ?pot))
    :effect (prepared ?location))

  (:action plant-it
    :parameters (?location - location ?plant - plant)
    :precondition (and (plant-available ?plant) (prepared ?location))
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
    :parameters (?plot - plot ?seed - seed)
    :precondition (and (plot-dug ?plot) (seed-available ?seed))
    :effect (and (growing ?plant) (planted ?seed ?plot)))

  (:action sprout
    :parameters (?plant - plant ?plot - plot ?seed - seed)
    :precondition (planted ?seed ?plot)
    :effect (and (growing ?plant ?plot) (sprout-in-plot ?plant ?plot)))

  (:action transition-to-flowering
    :parameters (?plant - plant ?plot - plot)
    :precondition (and (growing ?plant) (alive ?plant))
    :effect (flowering ?plant))

  (:action harvest
    :parameters (?plant - plant ?plot - plot)
    :precondition (and (planted ?plant ?plot) (flowering ?plant) (alive ?plant))
    :effect(and (not (planted ?plant ?plot)) (not (alive ?plant)) (not (growing ?plant)) (harvested ?plant)))

  (:action dry
    :parameters (?plant - plant ?plot - plot ?curing-container - curing-container )
    :precondition (harvested ?plant)
    :effect(and (plant-drying ?plant) (plant-in-curing-container ?plant ?curing-container)))

  (:action water
    :parameters (?plant - plant ?water-can - water-container ?location - location)
    :precondition (and (alive ?plant) (water-container-available ?water-can) (not (empty ?water-can)))
    :effect (and (watered-plant ?plant) (not (dry ?location)) (empty ?water-can)))

  (:action apply-mulch
    :parameters (?plot - plot ?mulch - mulch)
    :precondition (and (plot-dug ?plot) (mulch-available ?mulch))
    :effect (mulched ?plot))

  (:action dig-soil
    :parameters (?plot - plot ?digging-tool - tool)
    :precondition (and (prepared ?plot) (not (plot-dug ?plot)) (digging-tool-available ?digging-tool))
    :effect (plot-dug ?plot))

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

  (:action remove-weeds
    :parameters (?plot - plot ?plant - plant)
    :precondition (and (weeds ?plot) (growing ?plant) (planted ?plant ?plot))
    :effect (not (weeds ?plot)))

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
    :precondition (and (growing ?plant) (infested ?plot) (planted ?plant))
    :effect (not (infested ?plot)))

  (:action cover
    :parameters (?plant - plant ?plot - plot)
    :precondition (and (growing ?plant) (freezing-conditions ?plot) (not (covered ?plot)))
    :effect (covered ?plot))

  (:action add-support-structure
    :parameters (?plant - plant ?structure - support-structure)
    :precondition (and (growing ?plant) (support-structure-available ?structure))
    :effect (supported ?plant))

  (:action pollinate
    :parameters (?plant - plant ?pollinator - pollinator)
    :precondition (and (growing ?plant) (flowering ?plant) (pollinator-available ?pollinator))
    :effect (pollinated ?plant))
)