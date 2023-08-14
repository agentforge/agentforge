(define (domain garden)

  (:requirements :strips :typing :negative-preconditions)

  (:types
    plant - string
    seed clone - plant
    plot pot - location
    water-container curing-container - container
    container location tool amendment - boolean
    mulch fertilizer - amendment
  )

  (:predicates
    (prepared ?plot - plot)
    (flowering ?plant - plant)
    (watered-plant ?plant - plant)
    (mulched ?plot - plot)
    (plot-fertilized ?plot - plot)
    (infested ?plant - plant)
    (weeds ?plot - plot)
    (plot-dug ?plot - plot)
    (plant-in-plot ?plant - plant ?plot - plot)
    (seed-in-plot ?seed - seed ?plot - plot)
    (watered-plant ?plant - plant)
    (watered-seed ?seed - seed)
    (watered-plot ?plot - plot)
    (matured ?plant - plant)
    (alive ?plant - plant)
    (growing ?plant - plant)
    (digging-tool-available ?digging-tool - tool)
    (seed-available ?seed - seed)
    (clone-available ?clone - clone)
    (fertilizer-available ?fertilizer - fertilizer)
    (mulch-available ?mulch - mulch)
    (water-container-available ?water-can - water-container)
    (pot-available ?pot - pot)
    (empty ?water-can - container)
    (dry ?plot - plot)
    (unplanted ?plot - plot)
    (has-seed-type ?seed - seed ?plant - plant)
    (has-clone-type ?clone - clone ?plant - plant)
    (plant-in-container ?plant - plant ?water-can - water-container)
    (germinating ?seed - seed)
    (plant-in-curing-container ?plant - plant ?curing-container - curing-container)
    (plant-drying ?plant - plant)
    (freezing-conditions ?plot - plot)
  )

  (:action get-fertilizer
    :parameters (?fertilizer - fertilizer)
    :effect (fertilizer-available ?fertilizer))

  (:action get-digging-tool
    :parameters (?digging-tool - tool)
    :effect (digging-tool-available ?digging-tool))

  (:action dig-plot
    :parameters (?plot - plot ?digging-tool - tool)
    :precondition (and (digging-tool-available ?digging-tool) (unplanted ?plot) (dry ?plot))
    :effect (plot-dug ?plot))

  (:action get-seeds
    :parameters (?seed - seed ?plot - plot ?plant - plant)
    :precondition (and (has-seed-type ?seed ?plant))
    :effect (seed-available ?seed))

  (:action get-clone
    :parameters (?clone - clone ?plot - plot ?plant - plant)
    :precondition (and (has-clone-type ?clone ?plant))
    :effect (clone-available ?clone))

  (:action plant-seeds
    :parameters (?seed - seed ?plot - plot ?plant - plant)
    :precondition (and (seed-available ?seed) (plot-dug ?plot) (has-seed-type ?seed ?plant))
    :effect (and (seed-in-plot ?seed ?plot) (growing ?plant)))

  (:action plant-clone
    :parameters (?clone - clone ?plot - plot ?plant - plant)
    :precondition (and (clone-available ?clone) (plot-dug ?plot) (has-clone-type ?clone ?plant))
    :effect (and (plant-in-plot ?plant ?plot) (growing ?plant)))

  (:action fill-watering-can
    :parameters (?water-can - container)
    :precondition (and (water-container-available ?water-can) (empty ?water-can))
    :effect (not (empty ?water-can)))

  (:action move-to-pot
    :parameters (?plant - plant ?water-can - container ?plot - plot ?pot - pot)
    :precondition (and (plant-in-plot ?plant ?plot) (container-available ?pot))
    :effect (and (not (plant-in-plot ?plant ?plot)) (plant-in-container ?plant ?water-can)))

  (:action move-to-plot
    :parameters (?clone - clone ?plot - plot ?plant - plant)
    :precondition (and (plot-dug ?plot) (plot-fertilized ?plot) (mulched ?plot))
    :effect (and (plant-in-plot ?plant ?plot) (growing ?plant)))

  (:action prepare-pot
    :parameters (?plot - plot ?fertilizer - fertilizer)
    :effect (and (prepared ?plot) (plot-fertilized ?plot)))

  (:action prepare-plot
    :parameters (?plot - plot ?fertilizer - fertilizer)
    :effect (and (prepared ?plot) (plot-fertilized ?plot)))

  (:action germinate
    :parameters (?plot - plot ?water-can - water-container ?seed - seed)
    :precondition (prepared ?plot)
    :effect (and (germinating ?seed)))

  (:action sow
    :parameters (?plot - plot ?seed - seed)
    :precondition (and (plot-dug ?plot) (seed-available ?seed))
    :effect (and (growing ?seed ?plot) (seed-in-plot ?seed ?plot)))

  (:action sprout
    :parameters (?plant - plant ?plot - plot ?seed - seed)
    :precondition (seed-in-plot ?seed ?plot)
    :effect (and (growing ?plant ?plot) (sprout-in-plot ?plant ?plot)))

  (:action transition-to-flowering
    :parameters (?plant - plant ?plot - plot)
    :precondition (and (growing ?plant) (alive ?plant))
    :effect (flowering ?plant))

  (:action harvest
    :parameters (?plant - plant ?plot - plot)
    :precondition (and (plant-in-plot ?plant ?plot) (flowering ?plant) (alive ?plant))
    :effect(and (not (plant-in-plot ?plant ?plot)) (not (alive ?plant)) (not (growing ?plant)) (harvested ?plant)))

  (:action dry
    :parameters (?plant - plant ?plot - plot)
    :precondition (and (plant-in-plot ?plant ?plot) (flowering ?plant) (alive ?plant))
    :effect(and (not (plant-in-plot ?plant ?plot)) (not (alive ?plant)) (harvested ?plant)))

  (:action dry
    :parameters (?plant - plant ?plot - plot ?curing-container - curing-container )
    :precondition (harvested ?plant)
    :effect(and (plant-drying ?plant) (plant-in-curing-container ?plant ?curing-container)))

  (:action water
    :parameters (?plant - plant ?water-can - water-container)
    :precondition (and (alive ?plant) (water-container-available ?water-can))
    :effect (and (watered-plant ?plant) (not (dry ?plant))))

  (:action apply-mulch
    :parameters (?plot - plot ?mulch - mulch)
    :precondition (and (plot-dug ?plot) (mulch-available ?mulch))
    :effect (mulched ?plot))

  (:action prepare-soil
    :parameters (?plot - plot ?digging-tool - tool)
    :precondition (and (prepared ?plot) (not (plot-dug ?plot)) (digging-tool-available ?digging-tool))
    :effect (plot-dug ?plot))

  (:action amend-soil
    :parameters (?plot - plot ?fertilizer - fertilizer)
    :precondition (and (prepared ?plot) (plot-dug ?plot) (fertilizer-available ?fertilizer))
    :effect (plot-fertilized ?plot))

  (:action apply-fertilizer
    :parameters (?plot - plot ?fertilizer - fertilizer)
    :precondition (and (plot-dug ?plot) (fertilizer-available ?fertilizer))
    :effect (plot-fertilized ?plot))

  (:action apply-pesticide
    :parameters (?plant - plant ?pesticide - pesticide)
    :precondition (and (infested ?plant) (growing ?plant) (flowering ?plant) (alive ?plant) (pesticide-available ?pesticide))
    :effect (not (infested ?plant)))

  (:action remove-weeds
    :parameters (?plot - plot ?plant - plant)
    :precondition (and (weeds ?plot) (growing ?plant) (plant-in-plot ?plant ?plot))
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
    :precondition (and (growing ?plant) (infested ?plot) (plant-in-plot ?plant))
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