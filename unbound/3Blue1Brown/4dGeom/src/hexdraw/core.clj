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
;; use g
;; (.drawLine g 0 0 10 10)
;; (.drawLine g 0 150 150 0)

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

(defn draw-shape [shape gfx]
    (dorun (map draw-line-2d
        shape
        (concat (rest shape) [(first shape)])
        (repeat gfx)
    ))
)

(defn draw-ngon [n gfx screenify-fn color]
    (let [shape (unit-ngon n)
          screenified (screenify-fn shape)]
        (.setColor gfx color)
        (draw-shape screenified gfx)
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

(def drawn-pgon (draw-ngon 6 g (unit-to-screen 400 400 0.9) red))
(def arrangements (get-parallelagram-arrangements drawn-pgon))
(def pgram1 (get (get arrangements 0) 0))
(fill-shape-poly pgram1 blue "pgram1" g)

;; save:
(ImageIO/write bi "png"  (File. "test.png"))