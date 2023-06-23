

(define (problem depot48-problem)
  (:domain depot48)
  (:objects
    depot48-1-1 depot48-1-2 depot48-1-3 depot48-2-1 depot48-2-2 depot48-2-3
    container-0-0 container-0-1 container-0-2
    crate0 crate1 crate2
    container0
    depot48
    loadarea
    hoist0
  )
  (:init
    (adjacent depot48-1-1 depot48-1-2)
    (adjacent depot48-1-2 depot48-1-3)
    (adjacent depot48-2-1 depot48-2-2)
    (adjacent depot48-2-2 depot48-2-3)
    (in depot48 depot48-1-1)
    (in depot48 depot48-1-2)
    (in depot48 depot48-1-3)
    (in depot48 depot48-2-1)
    (in depot48 depot48-2-2)
    (in depot48 depot48-2-3)
    (in container0 container-0-0)
    (in container0 container-0-1)
    (in container0 container-0-2)
    (on container-0-0 crate0)
    (on container-0-1 crate1)
    (on container-0-2 crate2)
    (connected container-0-0 loadarea)
    (connected container-0-1 loadarea)
    (connected container-0-2 loadarea)
    (connected depot48-2-1 loadarea)
    (clear depot48-1-1)
    (clear depot48-2-1)
    (clear depot48-2-3)
    (clear depot48-1-2)
    (clear depot48-2-2)
    (available hoist0)
  )
  (:goal (and
    (in depot48 crate0)
    (in depot48 crate1)
    (in depot48 crate2)
  ))
)