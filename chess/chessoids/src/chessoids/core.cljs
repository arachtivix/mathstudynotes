(ns chessoids.core
    (:require react-dom))

(.render js/ReactDOM
  (.createElement js/React "h2" nil "Chessoids")
  (.getElementById js/document "app"))

(def k "king")
(def q "queen")
(def r "rook")
(def b "bishop")
(def n "knight")
(def p "pawn")

(def wh "white")
(def bl "black")

(def pieces {
    wh {k "♔" q "♕" r "♖" b "♗" n "♘" p "♙"}
    bl {k "♚" q "♛" r "♜" b "♝" n "♞" p "♟"}
})

(def canvas (.getElementById js/document "spooshl"))
(def ctx (.getContext canvas "2d"))

; (piece color rank)
(defn pc [c r] ((pieces c) r))

(defn draw-pc [c r x y px]
    (set! (.-fillStyle ctx) "rgb(0,0,255)")
    (.fillRect ctx x, y, px, px)
    (set! (.-fillStyle ctx) "rgb(255,0,0)")
    (set! (.-font ctx) (str px "px Roboto"))
    (.strokeText ctx (pc c r) x (+ px y))
)

(defn draw-tile [i j w h x y c1 c2]
    (let [active-color (if (= (mod i 2) (mod j 2)) c1 c2)
          t (+ y (* i w))
          r (+ x (* j h))]
        (set! (.-fillStyle ctx) active-color)
        (.fillRect ctx r, t, w, h)
    )
)

(defn draw-board []
    (for [i (range 8)
          j (range 8)]
          (draw-tile i j 50 50 100 100 "rgb(255,255,255)" "rgb(0,0,0)"))
)