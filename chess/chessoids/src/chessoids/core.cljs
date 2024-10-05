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

; (piece color rank)
(defn pc [c r] ((pieces c) r))

(defn draw-pc [c r px]
    (def canvas (.getElementById js/document "spooshl"))
    (def ctx (.getContext canvas "2d"))
    (set! (.-fillStyle ctx) "rgb(255,0,0)")
    (set! (.-font ctx) (str px "px Veranda"))
    (.strokeText ctx (pc bl q) 10 100)
)
