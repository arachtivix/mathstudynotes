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

(defn draw-pc [piece x y px]
    (set! (.-fillStyle ctx) "rgb(0,0,255)")
    (.fillRect ctx x, y, px, px)
    (set! (.-fillStyle ctx) "rgb(255,0,0)")
    (set! (.-font ctx) (str px "px Roboto"))
    (.strokeText ctx piece x (+ px y))
)

(defn gen-grid-coord-fn [origin-x origin-y grid-square-width grid-square-height]
    (fn [i j] [(+ origin-x (* grid-square-width i)) (+ origin-y (* grid-square-height j))])
)

(defn gen-fill-rect-grid [grid-fn w h context]
    (fn [i j color]
        (let [[x y] (grid-fn i j)]
            (set! (.-fillStyle ctx) color)
            (.fillRect context x y w h)
        )
    )
)

(def gcf (gen-grid-coord-fn 100 100 20 20))
(def basic-fill-rect (gen-fill-rect-grid gcf 20 20 ctx))

(defn draw-board []
    (for [i (range 8)
          j (range 8)]
          (basic-fill-rect i j (if (= (mod i 2) (mod j 2)) "rgb(255,255,255)" "rgb(0,0,0)")))
)