# Set linestyle 1 to blue (#0060ad)
set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 3 \
    pointtype 7 pointsize 1.5

# set terminal x11
# set terminal gif animate delay 10
# set output 'test.gif'
stats '~/Dropbox/machine_learning/session2/cversion/gnuplot/data.txt' nooutput

set xrange [0:100]
set yrange [0:100]

do for [i=1: int(STATS_blocks-1)] {
   plot '~/Dropbox/machine_learning/session2/cversion/gnuplot/data.txt' u 1:2 index i with linespoints linestyle 1
   pause 0.001
}
