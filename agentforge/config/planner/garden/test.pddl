
(define (problem user-problem)
    (:domain garden)
    (:objects 
        digging-tool - tool
        fertilizer - fertilizer
        cannabis-plant - cannabis-plant
        location - location
        og-kush - strain
        tool - tool
        strain - strain
        water-container - water-container
        curing-container - curing-container
        mulch - mulch
        amendment - amendment
        pesticide - pesticide
        biocontrol - biocontrol
        outdoor-plot - outdoor-plot
        support-structure - support-structure
    )
    (:init 
        (digging-tool-available digging-tool)
        (fertilizer-available fertilizer)
        (has-seeds cannabis-plant)
        (outdoor-plot-available location)
        (strain-chosen og-kush)
    )
    (:goal
        (and
            (growing cannabis-plant)
        )
    )
)
