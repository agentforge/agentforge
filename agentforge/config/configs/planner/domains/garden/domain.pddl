(define (domain garden)

  (:requirements :strips :typing)

  (:types
    plant seed plot container tool
    plot container - location
    fertilizer - object
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
    (growing ?p - plot ?plant - plant)
    (tool-available ?t - tool)
    (seed-available ?s - seed)
    (fertilizer-available ?f - fertilizer)
    (container-available ?c - container)
    (empty ?c - container)
    (dry ?p - plot)
    (unplanted ?p - plot)
    (has-seed-type ?s - seed ?plant - plant)
    (plant-in-container ?plant - plant ?c - container)
  )

  (:action dig-plot
    :parameters (?p - plot ?t - tool)
    :precondition (and (tool-available ?t) (unplanted ?p) (dry ?p))
    :effect (plot-dug ?p))

  (:action water-plot
    :parameters (?t - tool ?c - container ?p - plot)
    :precondition (and (plot-dug ?p) (tool-available ?t) (container-available ?c) (not (empty ?c)))
    :effect (and (watered ?p) (watered-plot ?p) (empty ?c)))

  (:action apply-fertilizer
    :parameters (?p - plot ?f - fertilizer)
    :precondition (and (plot-dug ?p) (fertilizer-available ?f))
    :effect (plot-fertilized ?p))

  (:action plant-seeds
    :parameters (?s - seed ?p - plot ?plant - plant)
    :precondition (and (seed-available ?s) (plot-dug ?p) (plot-fertilized ?p) (has-seed-type ?s ?plant))
    :effect (and (seed-in-plot ?s ?p) (growing ?p ?plant)))

  (:action fill-watering-can
    :parameters (?c - container)
    :precondition (and (container-available ?c) (empty ?c))
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
    :parameters (?plant - plant ?c - container ?p - plot)
    :precondition (and (plant-in-container ?plant ?c) (plot-dug ?p))
    :effect (and (not (plant-in-container ?plant ?c)) (plant-in-plot ?plant ?p) (growing ?p ?plant)))
)
