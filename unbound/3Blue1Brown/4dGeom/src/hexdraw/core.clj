(ns hexdraw.core
  (:import java.io.File)
  (:import java.awt.Color)
  (:import java.awt.image.BufferedImage)
  (:import javax.imageio.ImageIO)
  (:import java.lang.Math))

(def bi (BufferedImage. 400 400 BufferedImage/TYPE_INT_ARGB))
(def g (.createGraphics bi))
(def yellow (. Color yellow))
(def red (. Color red))
(def blue (. Color blue))
(def white (. Color white))

(defn unit-ngon [n]
    (map
        (fn [c] 
            [
                (Math/cos (* c 2.0 (/ (. Math PI) n)))
                (Math/sin (* c 2.0 (/ (. Math PI) n)))
            ]
        )
        (range n)
    )
)

(defn scale-2d [shape factor]
    (map (fn [[x y]] [(* factor x) (* factor y)]) shape)
)

(defn translate-2d [shape dx dy]
    (map (fn [[x y]] [(+ x dx) (+ y dy)]) shape)
)

(defn unit-to-screen [sw sh pad]
    (let [cx (/ sw 2)
          cy (/ sh 2)]
        (comp
            (fn [shape] (translate-2d shape cx cy))
            (fn [shape] (scale-2d shape (* cx pad)))
        )      
    )
)

(defn draw-line-2d [from to gfx]
    (let [fx (get from 0)
          fy (get from 1)
          tx (get to 0)
          ty (get to 1)]
          (.drawLine gfx fx fy tx ty))
)

(defn draw-dots [from to gfx]
    (let [fx (get from 0)
          fy (get from 1)
          tx (get to 0)
          ty (get to 1)]
          (.drawLine gfx fx fy fx fy)
          (.drawLine gfx tx ty tx ty))
)

(defn draw-shape [shape gfx draw-fn]
    (dorun (map draw-fn
        shape
        (concat (rest shape) [(first shape)])
        (repeat gfx)
    ))
)

(defn draw-ngon [n gfx screenify-fn color]
    (let [shape (unit-ngon n)
          screenified (screenify-fn shape)]
        (.setColor gfx color)
        (draw-shape screenified gfx draw-line-2d)
        screenified
    )
)

(defn avg-pts [pts]
    (let [sumx (reduce + (doall (map #(get % 0) pts)))
          sumy (reduce + (doall (map #(get % 1) pts)))
          denom (count pts)]
    [
        (/ sumx denom)
        (/ sumy denom)
    ])
)

(defn get-parallelagram-arrangements [[h0 h1 h2 h3 h4 h5]]
    (let [center (avg-pts [h0 h3])]
        [
            [
                [h0 h1 h2 center]
                [h2 h3 h4 center]
                [h4 h5 h0 center]
            ]
            [
                [h1 h2 h3 center]
                [h3 h4 h5 center]
                [h5 h0 h1 center]
            ]
        ]
    )
)

(defn shape-to-java-arrays [shape]
    [
        (int-array (doall (map #(get % 0) shape)))
        (int-array (doall (map #(get % 1) shape)))
    ]
)

(defn fill-shape-poly [shape color label gfx]
    (let [[xs ys] (shape-to-java-arrays shape)
          [cx cy] (avg-pts shape)]
        (.setColor gfx color)
        (.fillPolygon gfx xs ys (count xs))
        (.setColor gfx white)
        (.drawString gfx label (float cx) (float cy))
    )
)

(defn subdivide-line [[x1 y1] [x2 y2] n]
    (cond (= n 0) [[x1 y1]]
          :else (let [dx (- x2 x1)
                    dy (- y2 y1)
                    ddx (/ dx n)
                    ddy (/ dy n)]
                    (for [i (range (+ n 1))]
                        [
                            (+ x1 (* i ddx))
                            (+ y1 (* i ddy))
                        ]
                    )
                )
    )
)

(defn subdivide-triangle [[p1 p2 p3] n]
    (let [left-leg (subdivide-line p1 p2 n)
          right-leg (subdivide-line p1 p3 n)]
        (set 
            (apply concat
                (map subdivide-line left-leg right-leg (range))
            )
        )
    )
)

(defn subdivide-hexagon [[p1 p2 p3 p4 p5 p6] n]
    (let [center (avg-pts [p1 p2 p3 p4 p5 p6])]
        (apply concat
            (subdivide-triangle [center p1 p2] n)
            (subdivide-triangle [center p2 p3] n)
            (subdivide-triangle [center p3 p4] n)
            (subdivide-triangle [center p4 p5] n)
            (subdivide-triangle [center p5 p6] n)
            [(subdivide-triangle [center p6 p1] n)]
        )
    )
)

;; most useful when the grid is perfectly aligned with the y axis of course
(defn sort-grid [grid]
    (reduce 
        (fn [ret [x y]]
            (let [inty (int y)
                  existing (get ret inty)]
                (if (nil? existing) (assoc ret inty '([x y]))
                    (assoc ret inty (cons [x y] existing)))
            )
        )
        {}
        grid
    )
)

(def drawn-pgon (draw-ngon 6 g (unit-to-screen 400 400 0.9) red))
(def arrangements (get-parallelagram-arrangements drawn-pgon))
(def pgram1 (get (get arrangements 0) 0))
(fill-shape-poly pgram1 blue "pgram1" g)
(def grid (subdivide-hexagon drawn-pgon 3))
(print (sort-grid grid))
(draw-shape grid g draw-dots)
(ImageIO/write bi "png"  (File. "test.png"))
