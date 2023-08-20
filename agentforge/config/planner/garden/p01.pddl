(define (problem garden-enhanced-problem)
 (:domain garden)
 (:objects 
      cannabis - seed
      cannabis - clone
      plot - plot
      hose - water-container
      trowel - digging-tool
      limited-water - watersource
 )
 (:init 
  (weeds plotA)
  (empty plotB)
 )
 (:goal
  (and
      (growing cannabis)
  )))
