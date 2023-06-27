(define (domain backyard-garden)

  (:requirements :strips :typing)

  (:types
    plant seed plot container tool gardener fertilizer - object
  )

  (:predicates
    (plot-dug ?p - plot)
    (plot-fertilized ?p - plot)
    (plant-in ?plant - plant ?location - (either plot container))
    (plant-watered ?plant - plant)
    (plant-matured ?plant - plant)
    (plant-alive ?plant - plant)
    (tool-available ?t - tool)
    (seed-available ?s - seed)
    (container-available ?c - container)
  )

  (:action dig-plot
    :parameters (?p - plot ?t - tool ?g - gardener)
    :precondition (and (tool-available ?t))
    :effect (and (plot-dug ?p) (not (tool-available ?t))))

  (:action plant-seeds
    :parameters (?s - seed ?p - plot ?g - gardener)
    :precondition (and (plot-dug ?p) (seed-available ?s))
    :effect (plant-in (plant-from-seed ?s) ?p))

  (:action water-plant
    :parameters (?plant - plant ?t - tool ?g - gardener)
    :precondition (and (plant-in ?plant ?p) (tool-available ?t))
    :effect (and (plant-watered ?plant) (not (tool-available ?t))))

  (:action apply-fertilizer
    :parameters (?p - plot ?f - fertilizer ?g - gardener)
    :precondition (plot-dug ?p)
    :effect (plot-fertilized ?p))

  (:action harvest
    :parameters (?plant - plant ?p - plot ?g - gardener)
    :precondition (and (plant-in ?plant ?p) (plant-matured ?plant))
    :effect (not (plant-in ?plant ?p)))

  (:action move-to-pot
    :parameters (?plant - plant ?c - container ?g - gardener)
    :precondition (and (plant-in ?plant ?p) (container-available ?c))
    :effect (and (not (plant-in ?plant ?p)) (plant-in ?plant ?c)))

  (:action move-to-plot
    :parameters (?plant - plant ?p - plot ?g - gardener)
    :precondition (and (plant-in ?plant ?c) (plot-dug ?p))
    :effect (and (not (plant-in ?plant ?c)) (plant-in ?plant ?p)))

  (:action prune-plant
    :parameters (?plant - plant ?t - tool ?g - gardener)
    :precondition (and (plant-in ?plant ?location) (tool-available ?t))
    :effect (not (tool-available ?t)))
)
