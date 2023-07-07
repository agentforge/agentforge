(define (domain garden)

  (:requirements :strips :typing :negative-preconditions)

  (:types
    plant seed seedling plot container tool fertilizer
    plot container - location
    water-container - tool
  )

  (:predicates
    (plot-dug ?p - plot)
    (plot-fertilized ?p - plot)
    (plant-in-plot ?plant - plant ?p - plot)
    (seed-in-plot ?seed - seed ?p - plot)
    (watered-plant ?plant - plant)
    (watered-seed ?seed - seed)
    (watered-plot ?p - plot)
    (matured ?plant - plant)
    (alive ?plant - plant)
    (growing ?plant - plant)
    (digging-tool-available ?t - tool)
    (seed-available ?s - seed)
    (seedling-available ?seedling - seed)
    (fertilizer-available ?f - fertilizer)
    (water-container-available ?c - water-container)
    (container-available ?c - container)
    (empty ?c - container)
    (dry ?p - plot)
    (unplanted ?p - plot)
    (has-seed-type ?s - seed ?plant - plant)
    (has-seedling-type ?s - seedling ?plant - plant)
    (plant-in-container ?plant - plant ?c - container)
  )

  (:action get-fertilizer
    :parameters (?f - fertilizer)
    :effect (fertilizer-available ?f))

  (:action get-digging-tool
    :parameters (?t - tool)
    :effect (digging-tool-available ?t))

  (:action dig-plot
    :parameters (?p - plot ?t - tool)
    :precondition (and (digging-tool-available ?t) (unplanted ?p) (dry ?p))
    :effect (plot-dug ?p))

  (:action water-plot
    :parameters (?t - tool ?c - container ?p - plot)
    :precondition (and (plot-dug ?p) (water-container-available ?c))
    :effect (and (watered-plot ?p) (empty ?c)))

  (:action apply-fertilizer
    :parameters (?p - plot ?f - fertilizer)
    :precondition (and (plot-dug ?p) (fertilizer-available ?f))
    :effect (plot-fertilized ?p))

  (:action get-seeds
    :parameters (?s - seed ?p - plot ?plant - plant)
    :precondition (and (has-seed-type ?s ?plant))
    :effect (seed-available ?s))

  (:action get-seedling
    :parameters (?seedling - seedling ?p - plot ?plant - plant)
    :precondition (and (has-seedling-type ?seedling ?plant))
    :effect (seedling-available ?s))

  (:action plant-seeds
    :parameters (?s - seed ?p - plot ?plant - plant)
    :precondition (and (seed-available ?s) (plot-dug ?p) (has-seed-type ?s ?plant))
    :effect (and (seed-in-plot ?s ?p) (growing ?plant)))

  (:action plant-seedling
    :parameters (?s - seedling ?p - plot ?plant - plant)
    :precondition (and (seedling-available ?s) (plot-dug ?p) (plot-fertilized ?p) (has-seedling-type ?s ?plant))
    :effect (and (seed-in-plot ?s ?p) (growing ?plant)))

  (:action fill-watering-can
    :parameters (?c - container)
    :precondition (and (water-container-available ?c) (empty ?c))
    :effect (not (empty ?c)))

  (:action harvest
    :parameters (?plant - plant ?p - plot)
    :precondition (and (plant-in-plot ?plant ?p) (matured ?plant))
    :effect (not (plant-in-plot ?plant ?p)))

  (:action move-to-pot
    :parameters (?plant - plant ?c - container ?p - plot)
    :precondition (and (plant-in-plot ?plant ?p) (container-available ?c))
    :effect (and (not (plant-in-plot ?plant ?p)) (plant-in-container ?plant ?c)))

  (:action move-to-plot
    :parameters (?seedling - seedling ?p - plot)
    :precondition (plot-dug ?p)
    :effect (and (plant-in-plot ?plant ?p) (growing ?seedling)))
)