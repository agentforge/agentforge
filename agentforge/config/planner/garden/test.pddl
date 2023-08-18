(define (problem garden-enhanced-problem)
(:domain garden)
(:objects 
tomatoes - plant
plotX - plot
containerX - container
)
(:init 
(dry plotX)
(unplanted plotX)
(container-available containerX)
)
(:goal
(and
(growing tomatoes)
)))
