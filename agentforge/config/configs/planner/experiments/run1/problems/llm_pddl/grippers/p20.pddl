

(define (domain transport-balls)
  (:requirements :strips :typing)
  (:types robot room ball - object)
  (:predicates (at ?r - robot ?l - room)
               (holding ?r - robot ?b - ball)
               (free ?r - robot))
  (:action move
    :parameters (?r - robot ?l1 ?l2 - room)
    :precondition (and (at ?r ?l1) (not (at ?r ?l2)))
    :effect (and (at ?r ?l2) (not (at ?r ?l1))))
  (:action pick
    :parameters (?r - robot ?b - ball ?l - room)
    :precondition (and (at ?r ?l) (free ?r) (not (holding ?r ?b)))
    :effect (and (holding ?r ?b) (not (free ?r))))
  (:action drop
    :parameters (?r - robot ?b - ball ?l - room)
    :precondition (and (holding ?r ?b) (at ?r ?l))
    :effect (and (free ?r) (not (holding ?r ?b)))))

(define (problem transport-balls)
  (:domain transport-balls)
  (:objects robot1 robot2 robot3 robot4 room1 room2 room3 ball1 ball2 - ball)
  (:init (at robot1 room1)
         (at robot2 room1)
         (at robot3 room1)
         (at robot4 room1)
         (free robot1)
         (free robot2)
         (free robot3)
         (free robot4)
         (not (holding robot1 ball1))
         (not (holding robot2 ball1))
         (not (holding robot3 ball1))
         (not (holding robot4 ball1))
         (not (holding robot1 ball2))
         (not (holding robot2 ball2))
         (not (holding robot3 ball2))
         (not (holding robot4 ball2))
         (at ball1 room2)
         (at ball2 room3))
  (:goal (and (at ball1 room2)
              (at ball2 room3))))