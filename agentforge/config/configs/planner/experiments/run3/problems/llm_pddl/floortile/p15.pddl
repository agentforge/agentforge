

(define (problem painting-problem)
  (:domain painting)
  (:objects
    tile_0-1 tile_0-2 tile_0-3 tile_0-4 tile_0-5
    tile_1-1 tile_1-2 tile_1-3 tile_1-4 tile_1-5
    tile_2-1 tile_2-2 tile_2-3 tile_2-4 tile_2-5
    tile_3-1 tile_3-2 tile_3-3 tile_3-4 tile_3-5
    tile_4-1 tile_4-2 tile_4-3 tile_4-4 tile_4-5
    tile_5-1 tile_5-2 tile_5-3 tile_5-4 tile_5-5
    robot1 robot2
    white black
  )
  (:init
    (at robot1 tile_3-4)
    (at robot2 tile_5-5)
    (color tile_0-1 white)
    (color tile_0-2 black)
    (color tile_0-3 white)
    (color tile_0-4 black)
    (color tile_0-5 white)
    (color tile_1-1 black)
    (color tile_1-2 white)
    (color tile_1-3 black)
    (color tile_1-4 white)
    (color tile_1-5 black)
    (color tile_2-1 white)
    (color tile_2-2 black)
    (color tile_2-3 white)
    (color tile_2-4 black)
    (color tile_2-5 white)
    (color tile_3-1 black)
    (color tile_3-2 white)
    (color tile_3-3 black)
    (color tile_3-4 white)
    (color tile_3-5 black)
    (color tile_4-1 white)
    (color tile_4-2 black)
    (color tile_4-3 white)
    (color tile_4-4 black)
    (color tile_4-5 white)
    (color tile_5-1 black)
    (color tile_5-2 white)
    (color tile_5-3 black)
    (color tile_5-4 white)
    (color tile_5-5 black)
    (gun-color robot1 white)
    (gun-color robot2 black)
  )
  (:goal (and
    (color tile_0-1 white)
    (color tile_0-2 black)
    (color tile_0-3 white)
    (color tile_0-4 black)
    (color tile_0-5 white)
    (color tile_1-1 black)
    (color tile_1-2 white)
    (color tile_1-3 black)
    (color tile_1-4 white)
    (color tile_1-5 black)
    (color tile_2-1 white)
    (color tile_2-2 black)
    (color tile_2-3 white)
    (color tile_2-4 black)
    (color tile_2-5 white)
    (color tile_3-1 black)
    (color tile_3-2 white)
    (color tile_3-3 black)
    (color tile_3-4 white)
    (color tile_3-5 black)
    (color tile_4-1 white)
    (color tile_4-2 black)
    (color tile_4-3 white)
    (color tile_4-4 black)
    (color tile_4-5 white)
    (color tile_5-1 black)
    (color tile_5-2 white)
    (color tile_5-3 black)
    (color tile_5-4 white)
    (color tile_5-5 black)
  ))
  (:action move
    :parameters (?robot ?from ?to)
    :precondition (and (at ?robot ?from) (not (at ?robot ?to)))
    :effect (and (at ?robot ?to) (not (at ?robot ?from)))
  )
  (:action paint
    :parameters (?robot ?tile ?color)
    :precondition (and (at ?robot ?tile) (gun-color ?robot ?color) (not (color ?tile ?color)))
    :effect (and (color ?tile ?color))
  )
  (:action change-gun-color
    :parameters (?robot ?color)
    :precondition (not (gun-color ?robot ?color))
    :effect (gun-color ?robot ?color)
  )
)