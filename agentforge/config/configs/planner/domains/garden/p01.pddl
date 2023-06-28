(define (problem garden-enhanced-problem)
 (:domain gardening)
 (:objects 
      plotA plotB plotC - plot
      cucumber-seeds pepper-seeds sunflower-seeds - seeds
      hose - container
      trowel small-rake - tool
      limited-water - watersource
 )
 (:init 
  (has-weeds plotA)
  (empty plotB)
  (empty plotC)
  (available cucumber-seeds)
  (available pepper-seeds)
  (available sunflower-seeds)
  (available trowel)
  (available small-rake)
  (available hose)
  (water-supply limited-water)
  (hose-off hose)
 )
 (:goal
  (and
      (planted plotA cucumber-seeds)
      (planted plotB pepper-seeds)
      (planted plotC sunflower-seeds)
      (watered plotA)
      (watered plotB)
      (watered plotC)
      (hose-off hose)
      (available trowel)
      (available small-rake)
  )))
