(define (problem blockProblem)
(:domain blockWorld)
(:objects A B C D - block)
(:init (ontable A)
(ontable D)
(on B A)
(clear B)
(on C D)
(clear C)
(handempty))
(:goal (and (on A B) (on B C) (on C D) (clear A) (handempty)))
)
