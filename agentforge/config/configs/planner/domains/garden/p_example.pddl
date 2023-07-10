(define (problem garden-problem)
  (:domain garden)
  (:objects 
      plot1 plot2 plot3 - plot
      watering-can - container
      tomato-seeds - seed
      carrot-seeds - seed
      fertilizer - object
      shovel - tool
  )
  (:init 
      (empty watering-can)
      (dry plot1)
      (dry plot2)
      (dry plot3)
      (unplanted plot1)
      (unplanted plot2)
      (unplanted plot3)
      (has-seed-type tomato-seeds tomatoes)
      (has-seed-type carrot-seeds carrots)
      (container-empty watering-can)
  )
  (:goal
      (and
          (growing plot1 tomatoes)
          (growing plot2 carrots)
          (watered plot1)
          (watered plot2)
          (unplanted plot3)
      )
  )
)
