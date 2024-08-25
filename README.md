# 08/23

## 基本アイデア
範囲内の値集合に関する一致判定が重要なので、ZobristHashだろう。
部分集合として含むかどうかなので、愚直にチェックするしかない。$L_B \leq 24$なのでまあ間に合う。

### ツアーパスの構築
目的地間は最短距離で移動するのでいいだろう。余計な迂回路のハンドリングは難しい。
強いていえば過去に通過した回数が多い道を好むくらいか。
その場合でも、目的地との距離が増加するようなことはあってはならない。

一部の来訪頂点だけで最小全域木を作って高速道路にして、地道はインターチェンジ降りる方式にしたら明確に利用頻度が別れるのでは、
最小全域木に使う頂点は、子頂点との最大距離を最小化するクラスタリングとか。

### 辞書$A$の構築
移動ごとに毎回信号を切り替える非効率なツアーを基準に考えると、確定したツアー内の区間集合と$A$の連続部分列区間集合が一致することの相対的な嬉しさは、$(ツアー内区間の長さ - 1) \times 全ツアーパス内の出現回数$でざっくり見積れるだろう。なので
1. ツアー内の区間を$O(N^2)$で全探索して、その集合Hashの出現回数を数え上げ、上記の指標で降順ソートする。
1. ソート先頭から$A$に登録していく。
1. ツアーパス内に出現する頂点番号はすべて出現させたい。容量ギリギリになってきたら未登場の頂点番号を詰め込んでいく。

### 実際のプランニング
ツアーパスと辞書を固定すると、最適なプランニングはDPで求まる。
辞書内の任意の連続区間であって、長さ$L_B$の範囲には、必ず値重複がないという仮定のもとで

1. 事前に辞書内の長さ$L_b$以下の区間について、集合のHash値を求め、Setに格納しておく。計算量は$O(N\ L_B)$。
1. $DP[i]$を、ツアー内の$i$番目の地点へ到達するまでに必要な最小の信号変更回数とする。$i$から$j(i<j)$への繊維が可能かどうかは、区間$(i, j]$内に存在する頂点番号のHash値が辞書内に存在すること。計算量は$O(N^2)$
1. BackTraceによる実際のツアープロセス復元。

でも固定ツアーパスを忘れたDijkstraの方がよさそうだ

# 08/24

最初のツアーパス構築において、何度も通っている頂点を好むにしたら多少上がった。
信号は頂点ごとなので見落としていたが、集合として指定する以上はエッジこそが重要。
ただ、利用頻度の高い頂点ではなくエッジに着目したら、ほぼ変わらず少し下がったくらい。

でも問題点は青信号集合があまりにバラバラなこと。次案は
中心付近のエッジが重要なんだろうから、中心から信号集合の道をを連結してつなげていく処理を最初にやったほうがいいのでは

# 08/25
今までの方針を全部捨てて、グラフをサイズ$L_B$ごとの部分集合に分割して、その集合間をまたぐのがコストだと見なしてやったらめっちゃよくなった。
部分集合は中心からのユークリッド距離が小さいものからつなげていく処理を書いた。ちょっとつぶれすぎな気もしなくもないけど、
単純なBFS順よりも若干良い。
あとやれることとしては、$L_A$が$N$よりも大きい場合にそれをどう使うか。
$N$までと同じ部分集合作っても仕方ないから、離れた部分集合どうしをワープするような細長い高速道路が必要な気がする。