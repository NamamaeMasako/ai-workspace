# 驚蟄 / script.rpy

# 立繪演出以本檔的 show / hide 註記為準；立繪清單由實際使用標籤反向彙整。

label splashscreen:
    return

label before_main_menu:
    return

label start:
    scene black
    with fade

    centered "《驚蟄》\n全年齡展示版\n\n目前收錄：序章～第六章\nR18 內容暫不收錄。"

    jump prologue

label prologue:
    scene bg road_twilight
    with fade

    narrator "春末，紅原州的風帶著穀物的甜味，藍川州的潮氣則在遠處的山腳盤旋。"
    narrator "驚蟄踩著木屐，沿著兩州交界的舊道向前。"

    show jingzhe smoking at zh_center
    narrator "他看起來不像適合長途旅行的人：眼下烏黑，髮尾散亂，煙斗的煙在風裡斷斷續續。"

    jingzhe "……"

    narrator "煙草燃起時，他沒有想太多。"
    narrator "只是因為他喜歡。"

    show jingzhe pensive at zh_center
    narrator "他寫的故事總帶著陰影，卻又在陰影裡留一點溫度。"
    narrator "不是為了取悅誰，只是因為他喜歡。"

    narrator "遠處山腰間，一間旅店的屋簷在暮色裡浮出輪廓。"
    narrator "月下庄。"

    scene bg inn_exterior
    with dissolve

    narrator "旅店比他想像得更安靜。"
    narrator "他推門而入時，木鈴輕輕響了一下，像有人貼在耳邊低聲說：『來了。』"

    show hanami bright at zh_far_left
    hanami "歡迎光臨！旅人先生，要住店嗎？"

    show jingzhe neutral at zh_center
    jingzhe "……一晚。"

    hanami "一晚也行，不過這裡很安靜，很多人住了就捨不得走喔。"

    narrator "女孩的聲音帶著一點笑意，像是對陌生人天生就沒什麼距離。"
    narrator "他不討厭這種距離。"

    show yumemi shy at zh_far_right
    yumemi "姐姐，茶已經煮好了。"

    hanami "啊，對。先坐一下，我們給你倒茶。"

    narrator "另一名女孩把茶端來，視線不敢多停留，卻又忍不住在他手上的煙斗停了半秒。"
    narrator "驚蟄注意到了。"

    jingzhe "……你們不討厭煙？"

    yumemi "不會。只是……有點特別。"

    narrator "他很輕地笑了一下。"
    show jingzhe faint_smile at zh_center
    narrator "然後他知道，自己大概會在這裡住上一陣子。"

    jump chapter_1
label chapter_1:
    scene bg inn_morning
    with dissolve

    narrator "清晨的月下庄有一種乾淨的味道。"
    narrator "木地板的光澤被擦得剛剛好，既不刺眼，也不讓人覺得刻意。"

    show jingzhe pensive at zh_center
    narrator "驚蟄醒得比自己想像中還早。"

    jingzhe "……"

    narrator "他坐起身，手摸到床邊的煙斗，卻停了半秒。"
    narrator "這裡的空氣太淡，淡得很適合不去抽。"

    show hanami bright at zh_far_left
    hanami "早安！今天的早餐有紅玉粥跟醃漬魚，要不要試試看？"

    jingzhe "……都可以。"

    narrator "他不習慣被人用這種熱度對待。"
    narrator "但花見笑得理所當然，像世界上本來就該有人在早晨問你要不要吃粥。"

    show yumemi gentle at zh_far_right
    yumemi "我也煮了清茶，如果你不喜歡甜味，可以配這個。"

    yumemi "還有……你這件浴衣很好看。顏色很特別。"

    jingzhe "……我母親做的。"

    jingzhe "所以才一直穿著。"

    narrator "夢見怔了一下，像是沒想到他會這樣直接回答。"
    show yumemi surprised at zh_far_right

    jingzhe "謝謝。"
    show jingzhe softened at zh_center

    narrator "夢見的聲音像一點點柔軟的霧，停在每個音節之間。"

    scene bg inn_dining
    with dissolve

    narrator "早餐結束後，花見忙著打掃、換被單，夢見去整理後院的花草。"
    narrator "驚蟄坐在走廊邊，筆記本攤在膝上。"

    show jingzhe smoking at zh_center
    narrator "他沒有立刻寫字，只是讓煙斗的火慢慢燒著。"

    jingzhe "……"

    narrator "他記得自己的喜好。"
    narrator "陰鬱、潮濕、帶著孤獨的溫度。"

    narrator "那是他最熟悉的東西。"

    narrator "但他偶爾還是會在結尾留一個人，像是還在等誰。"

    show hanami curious at zh_far_left
    hanami "欸，你在寫小說對吧？"

    jingzhe "……嗯。"

    hanami "很厲害耶。這裡偶爾會有旅人帶小說來換故事，你的名字我好像看過。"

    jingzhe "不一定是我。"

    narrator "他不太喜歡被認出來。"
    narrator "但花見沒有追問，只是把抹布搭在肩上，靠著欄杆看他。"

    hanami "反正你喜歡這裡就好。住久一點也可以。"

    narrator "她說這句話時，像邀請，也像通知。"

    show yumemi gentle at zh_far_right
    narrator "夢見端著洗好的杯子路過，視線落在他的筆記本上。"

    yumemi "……如果你需要安靜的地方，後院有一棵老樹。坐在那裡很好寫東西。"

    jingzhe "知道了。"

    scene bg inn_backyard
    with dissolve

    narrator "後院比前院更安靜，只有水聲和風聲。"

    show jingzhe pensive at zh_right
    narrator "他坐在老樹下，翻開本子。"

    narrator "『他總是被討厭。』"

    narrator "他在第一行寫下這句話，又劃掉。"

    narrator "太直白了。"

    narrator "他重新寫："

    narrator "『他一直覺得，自己很難被好好留下。』"

    narrator "這句話比較像他自己。"
    narrator "也比較像這個世界。"

    show hanami bright at zh_left
    hanami "哎呀，你在這裡。"

    narrator "花見帶著一把長形的包布，像是習慣性背著。"

    jingzhe "那是？"

    hanami "薙刀。暮春大姊留下來的，平常不太用，怕生鏽。"

    jingzhe "妳能使？"

    hanami "會一點。"

    narrator "她說『一點』時，眼睛裡有那種很乾脆的自信。"
    narrator "像是承認自己會輸，卻不會怕。"
    show hanami determined at zh_left

    narrator "花見低頭擦過刀柄，指腹在舊傷似的刻痕上停了一下。"
    show hanami concerned at zh_left

    hanami "春姊很厲害，以前我總覺得，只要有危險，春姊都會保護我們。"

    hanami "後來春姊去了北方才發現，不是每次都能躲在春姊後面。"

    jingzhe "……所以妳才練？"

    hanami "嗯，春姊很會教呢。這樣至少真的有事的時候，我想讓自己能夠往前站。"

    scene bg inn_hall_evening
    with dissolve

    narrator "傍晚時分，月下庄的燈被點起來。"

    show yumemi gentle at zh_far_right
    yumemi "今晚要不要試試甜酒？我調得比較淡。"

    show jingzhe neutral at zh_center
    jingzhe "……好。"

    narrator "他喝了一口，味道柔軟，像一個讓人放鬆的理由。"

    show hanami bright at zh_far_left
    hanami "你看吧，住久一點也不會吃虧。"

    jingzhe "……也許。"

    narrator "他本來想說『再看看』。"
    narrator "但最後說出口的，只是一句含糊的肯定。"

    narrator "月下庄的夜很安靜。"

    narrator "安靜到他聽見自己的呼吸，聽見煙草的聲音，也聽見某種看不見的東西在遠處蠢動。"

    jump chapter_2
label chapter_2:
    scene bg inn_room_night
    with dissolve

    narrator "夜更深時，月下庄的走廊會安靜得像一條沒有人的河。"

    show jingzhe smoking at zh_center
    narrator "驚蟄坐在房裡，桌上只有一盞燈、一盒菸草，還有他那本磨舊的筆記。"

    jingzhe "……"

    narrator "他一直都是這樣寫的。"
    narrator "不是因為誰要求，也不是因為誰期待。"
    narrator "只是因為他喜歡。"

    show jingzhe pensive at zh_center
    narrator "煙草點燃時，房間裡的影子也跟著變深。"

    narrator "他聞到那股熟悉的味道，像是能把所有人隔在門外。"

    narrator "隔在門外也好。"

    narrator "從小到大，大家都怕他。"

    narrator "操蟲使是血脈傳下來的能力，強大，也讓人厭惡。"

    narrator "那些被排擠的日子，最後只教會他一件事："

    narrator "不要靠近別人。"

    narrator "靠近了，也只是讓自己更容易被討厭。"

    show jingzhe grief at zh_center
    narrator "他寫過很多這樣的角色。"

    narrator "孤獨、潮濕、帶著某種無法觸碰的欲望。"

    narrator "他總會在那欲望裡寫下一個名字，卻不敢讓任何人知道。"

    narrator "像是他自己。"

    scene bg inn_room_late
    with fade

    narrator "桌上有一個黑色的小盒子。"

    narrator "影之魔女送的魔法郵箱。"

    narrator "放進去的東西，會直接送到她的所在地。"

    narrator "她偶爾會回信。"

    narrator "短短幾行字裡，總會提到她不喜歡蟲子。"

    narrator "他不需要去找她，也不用親眼承受那種討厭。"

    narrator "這樣很好。"

    show jingzhe pensive at zh_center
    narrator "他把今天寫好的一頁紙折起，放進郵箱。"

    narrator "盒蓋闔上的瞬間，紙就消失了。"

    narrator "有時候，他會想："

    narrator "如果沒有這個盒子，自己還會不會寫下去。"

    narrator "答案他不願意去想。"

    narrator "雖然父親總是期待他的新稿，也會替他拿去出版，但真正能讀到最新一頁的，也就只剩影之魔女了。"

    narrator "可不管有沒有人在等，他都還是會寫。"

    narrator "因為寫作是他唯一的紓壓方式。"
    narrator "也是他還沒沉下去的理由。"

    scene bg inn_room_night
    with dissolve

    show jingzhe pensive at zh_center
    narrator "他合上筆記本時，窗外傳來幾聲蟲鳴。"

    narrator "那聲音沒有惡意，反而像是在提醒他："

    narrator "你並不孤單。"

    jingzhe "……"

    narrator "此時門外傳來很輕的腳步聲。"

    yumemi "我放一壺茶在門邊。"

    jingzhe "……不用特地沏茶的。"

    narrator "夢見沒有立刻離開。"

    yumemi "希望您別介意，是我願意幫您沏的。"

    narrator "她的視線落在桌上的黑色小盒子，又很快移開。"

    yumemi "如果有任何事，只要您願意說，我都願意聽。"

    narrator "她停了一下，聲音放得更輕。"

    yumemi "即便是難以啟齒或是危險的事……我都會沏好茶等您說的。"

    jingzhe "……"

    jingzhe "知道了。"

    narrator "他看著窗外的夜色，沒有回應。"

    narrator "但他知道，自己已經不是原來那個只會躲起來的人了。"
    narrator "至少，在這間旅店裡，他還願意留下。"

    jump chapter_3
label chapter_3:
    scene bg tavern_night
    with fade

    narrator "半年前的夜晚，比現在更悶熱。"
    narrator "驚蟄坐在小酒館的角落，煙斗裡的火光忽明忽暗。"

    show jingzhe smoking at zh_left
    narrator "那天他沒有特別想喝酒，只是需要一個不會被打擾的地方。"

    jingzhe "……"

    narrator "杯底見光時，有人坐到了他的對面。"

    show achirichi calm at zh_right
    achirichi "介意嗎？"

    jingzhe "……隨便。"

    narrator "對方看起來不像醉漢，衣著整齊，眼神也太乾淨。"

    achirichi "我叫亞奇里奇。"

    jingzhe "聽起來不像本地名。"

    achirichi "不是。"

    narrator "他把一張全黑的卡片放在桌上。"

    achirichi "我來，是因為你會需要它。"

    jingzhe "這種推銷很老套。"

    achirichi "不是推銷。"

    narrator "亞奇里奇的聲音很穩，像是早就把某件事算好了。"

    achirichi "影之魔女是我的老師。"

    show jingzhe wary at zh_left
    jingzhe "……"

    narrator "驚蟄沒有抬頭，但手指停在煙斗上。"

    achirichi "她很喜歡你的小說。"

    jingzhe "她不喜歡蟲。"

    achirichi "所以她才用郵箱。"

    narrator "那句話像提醒，也像確認。"

    achirichi "卡片會保護持有它的人。"
    show achirichi serious at zh_right

    jingzhe "怎麼保護？"

    achirichi "撕開就知道了。"

    narrator "他沒有伸手去拿。"

    jingzhe "我不想欠她人情。"

    achirichi "你不欠她。"

    achirichi "她只是想讓你繼續寫。"
    show jingzhe shocked at zh_left

    narrator "那句話落下時，驚蟄的喉嚨動了一下。"
    narrator "他不確定那是不是自己的軟肋。"

    jingzhe "我會自己照顧自己。"
    show jingzhe stern at zh_left

    achirichi "我知道。"

    narrator "亞奇里奇把卡片推近了一點。"

    achirichi "但你不是每次都能照顧好你自己。"

    narrator "桌面上那張黑色的卡，像一塊沒有溫度的夜。"

    narrator "驚蟄終於把它收進袖口。"

    jingzhe "……這筆帳記在她身上。"

    achirichi "不，記在你自己身上。"

    narrator "亞奇里奇站起身。"

    achirichi "不要把卡片交給別人。"

    narrator "驚蟄沒有回答，只是低頭續火。"

    narrator "等他再抬頭時，人已經走了。"

    narrator "那晚，酒意散得很慢，熱氣卻一點也沒退。"

    jump chapter_4
label chapter_4:
    scene bg inn_exterior_twilight
    with dissolve

    narrator "入夜前的風變得濕。"

    narrator "月下庄的燈在風裡輕晃，像是有人用指尖撥動。"

    show jingzhe wary at zh_center
    narrator "驚蟄站在門口，煙斗沒有點。"

    jingzhe "……"

    narrator "他聽見了。"

    narrator "不是聲音，而是一種被注視的重量。"

    scene bg forest_path
    with fade

    narrator "同一時間，遠處的林道上，有東西正在移動。"

    narrator "泥土被壓得很深，卻沒有腳印留下。"

    show tsuchigumo looming at zh_far_left
    narrator "土蜘蛛貼著林道旁的樹幹移動。"
    narrator "牠巨大得像一座黑丘，枝葉卻沒有因牠的重量發出半點聲響。"
    narrator "只有偶爾垂落的蛛腳，從月光邊緣一閃而過。"

    show jorogumo watchful at zh_far_right
    narrator "土蜘蛛的身上，站著一名白衣女人。"
    narrator "她的輪廓像披著白無垢的新娘，頭上的棉帽低低壓著，其下透出數點陰森的光。"
    narrator "月光落在她身上時，沒有照出衣縫，只照出一層無聲、且濕冷的白。"
    narrator "她有節奏地轉著頭，像是焦急地尋找著某個人；可那銳利的視線裡沒有思念，只有捕食前的冷意——她要找的，絕不會是她的夫君。"

    narrator "當月下庄進入牠們的視野時，絡新婦抬起袖口，在空中停了一瞬 ，土蜘蛛也停了下來。"
    narrator "從絡新婦的袖口中，爬出細得幾乎看不見的東西，無聲落進草叢。"

    narrator "牠們都知道目的。"
    narrator "那個帶著煙草味的男人。"
    narrator "以及他身上的郵箱。"

    scene bg inn_hall_evening
    with dissolve

    show hanami concerned at zh_far_left
    hanami "你今天有點安靜喔？"

    show jingzhe wary at zh_center
    jingzhe "……嗯。"

    narrator "花見把餐盤放下，順手替他把燈拉亮了一點。"

    show yumemi worried at zh_far_right
    yumemi "是不是睡不好？"

    jingzhe "沒有。只是……"

    narrator "他停了一下。"

    narrator "他其實說得出口：有東西靠近了。"

    narrator "但這句話太像怪談，也太像麻煩。"

    jingzhe "只是風變了。"

    narrator "夢見點點頭，沒有再問。"
    narrator "她們都很自然地接受他的沉默。"

    scene bg inn_corridor_night
    with fade

    narrator "夜更深時，走廊裡的燈滅了一盞。"

    narrator "不是故障，像是被什麼不小心遮住。"

    show jingzhe wary at zh_center
    narrator "驚蟄走過時，指尖掠過牆面。"

    narrator "牆上有一點極細的白線，像蜘蛛絲，又像劃痕。"

    jingzhe "……"

    narrator "他沒有去碰。"
    narrator "也沒有告訴任何人。"

    scene bg inn_room_night
    with dissolve

    narrator "回到房裡，他把窗關上。"

    narrator "煙斗在掌心被握了一下，沒有點火。"

    narrator "他知道，真正靠近的不是今晚。"

    narrator "而是再過不久的某個夜晚。"

    narrator "他只是還不知道，那夜要付出的代價會是誰。"

    jump chapter_5
label chapter_5:
    scene bg inn_hall_evening
    with dissolve

    narrator "那幾天，月下庄的空氣比平常更黏。"

    narrator "像是有什麼看不見的絲，繞在走廊與房門之間。"

    show jingzhe wary at zh_center
    narrator "驚蟄沒說出口，但他知道，這不是天氣的問題。"
    narrator "連風都像被誰收窄了。"

    scene bg inn_hall_evening
    with dissolve

    show hanami possessed_sweet at zh_left
    hanami "你今天也在寫？"

    show jingzhe wary at zh_right
    jingzhe "……嗯。"

    narrator "花見的聲音依舊明亮，但那份熱度裡，多了一點刻意。"

    narrator "她沒有像平常那樣站在欄杆旁，而是直接繞到他身側。"

    narrator "近得像只要他一轉頭，就會碰到她的髮尾。"

    hanami "你最近都不怎麼看我。"

    jingzhe "……有嗎。"

    narrator "花見低下身，手指落在他肩上。"
    show hanami possessed_blank at zh_left

    narrator "力道不重，卻像在確認他會不會照著她要的方向轉頭。"

    hanami "有啊。"

    hanami "還是你比較喜歡人家再靠近一點？"

    narrator "她笑著說。"
    narrator "笑得太甜，甜得像不是她。"

    jingzhe "……妳還好嗎？"
    show jingzhe wary at zh_right

    hanami "當然好呀。"

    narrator "回答太快，像背好的句子。"

    narrator "驚蟄的指尖輕輕敲了兩下桌面，像在確認某個節拍。"

    narrator "他瞥見她袖口邊緣有一點極細的白絲。"

    narrator "像不小心沾上的。"
    narrator "又像是誰故意留下的記號。"

    narrator "他沒有戳破，只是把視線移開。"

    narrator "他知道，一旦說出『不對勁』三個字，就會把她們推進更危險的中心。"

    scene bg inn_room_night
    with dissolve

    narrator "夜裡，花見敲了他的門。"

    show hanami possessed_sweet at zh_left
    hanami "可以進來嗎？"

    jingzhe "……進來吧。"
    show jingzhe wary at zh_right

    narrator "她走進來時沒有先說話。"

    narrator "只把門輕輕帶上。"

    narrator "那個動作讓房裡忽然太安靜了。"

    narrator "她的步伐很輕，眼神卻像被線牽著。"
    show hanami possessed_blank at zh_left

    narrator "她一路走到他面前，膝蓋幾乎碰上他的腿。"

    hanami "你今天身上……好香。"

    narrator "她低頭去聞他衣領邊的味道。"

    narrator "下一秒，一隻手摸上他的衣帶。"

    narrator "另一隻手卻沒有停在他身上。"
    narrator "而是沿著桌邊，往那個黑色小盒子的方向慢慢探去。"

    show jingzhe stern at zh_right
    narrator "那一瞬間，他很想伸手把她拉回來。"

    narrator "但他知道，碰觸太近只會讓對方陷得更深。"

    narrator "驚蟄聞到那股更細、更尖的味道。"

    narrator "不是花見平常會有的氣味。"

    narrator "像潮濕角落裡，很多小東西同時醒著。"

    hanami "你不喜歡我碰你嗎？"
    show hanami possessed_sweet at zh_left

    narrator "她抬眼看他。"

    narrator "那個眼神太直，也太空。"
    narrator "像她正在努力扮演自己。"

    narrator "但她指尖的方向出賣了她。"

    narrator "她真正想碰的，不是他。"

    show jingzhe battle at zh_right
    narrator "他把煙斗放到唇邊，沒有點燃。"

    narrator "只用指尖摩挲著煙草。"

    narrator "房間裡的氣味微微變了。"

    narrator "花見的動作一頓。"

    narrator "她摸著他衣帶的手停住。"

    narrator "而那隻快要碰到盒子的手，忽然一緊。"

    narrator "下一瞬，指尖的角度變了。"

    narrator "不是去拿。"
    narrator "而是猛地往他喉間一壓。"

    narrator "香味再重一點。"

    narrator "窗邊傳來一聲極細的裂響。"

    narrator "像有什麼小東西從梁上掉下去。"

    show hanami shaken at zh_left
    hanami "……我剛剛在做什麼？"

    narrator "她的眼神清了一點，像是終於從深水裡浮上來。"

    narrator "等她看見自己的手正抓著他的衣帶時，整張臉都白了一下。"

    jingzhe "不是妳。"

    narrator "驚蟄沒有多說，只把窗開了一道縫，讓冷風進來。"

    narrator "花見站在原地，像還沒從某場夢裡完全醒過來。"


    scene bg inn_hall_evening
    with dissolve

    narrator "隔天，輪到夢見變得不自然。"

    show yumemi possessed_blank at zh_left
    yumemi "我……可以幫你整理行李嗎？"

    show jingzhe wary at zh_right
    jingzhe "不用。"

    narrator "夢見點頭，卻沒有退開。"

    narrator "她的視線落在桌上那個黑色的小盒子上，停得太久。"

    narrator "和昨晚花見不同。"

    narrator "夢見沒有繞，也沒有演。"

    narrator "那股控制落在她身上，顯得更急、更粗糙，像只想快點把東西拿到手。"

    yumemi "那個……很重要嗎？"

    jingzhe "嗯。"

    narrator "她走近一步。"

    narrator "步子很輕，輕得像怕驚動誰。"

    narrator "但她的眼神卻不像在看一個盒子。"
    narrator "比較像在看某個被人下令一定要帶走的東西。"

    narrator "她的手指伸出去。"

    narrator "這一次，不是試探。"
    narrator "而是直接去拿。"

    show jingzhe stern at zh_right
    narrator "驚蟄伸手按住了她的手腕。"

    jingzhe "……那不是妳的。"

    narrator "夢見的身體僵了一下，像是被誰猛地拉住。"

    narrator "她抬頭看他，眼裡閃過一瞬間的慌。"

    narrator "她像想靠近，又像不知道自己為什麼會想靠近。"

    narrator "肩膀只輕輕碰到他的手臂，就停住了。"

    show yumemi possessed_blank at zh_left
    yumemi "那你……抱我一下，好不好？"

    narrator "她的聲音發顫。"

    narrator "不是平常那種害羞。"
    narrator "更像是有人在背後提著線，要她繼續做下去。"

    narrator "她的另一隻手還想去碰那個盒子。"

    narrator "驚蟄看見她指尖上黏著一點極淡的白絲。"

    narrator "和昨晚花見袖口上的一模一樣。"

    narrator "他再一次摩挲煙草。"

    narrator "那股細尖的味道被壓下去。"

    narrator "夢見像被人從背後剪斷了線，整個人晃了一下。"
    show yumemi frightened at zh_left

    narrator "她收回手，指尖發抖，連呼吸都亂了。"

    show yumemi ashamed at zh_left
    yumemi "我不知道……為什麼會想拿。"

    narrator "她的聲音帶著恐懼，也帶著困惑。"

    narrator "等她意識到自己剛才還說了什麼，耳尖一下紅得發燙。"

    narrator "可那紅不是害羞。"
    narrator "更像羞恥。"

    jingzhe "不是妳的意思。"

    narrator "驚蟄這次說得更直接。"

    narrator "因為再不說，她可能會把所有責任都往自己身上背。"


    scene bg inn_corridor_night
    with fade

    narrator "那晚，走廊的燈滅了一盞。"

    narrator "驚蟄在門縫下看見一截細細的影子。"

    narrator "像是蜘蛛的腳，又像是被風拉長的黑線。"

    narrator "他這次沒有立刻追出去。"

    narrator "因為他知道，對方已經開始急了。"

    show jorogumo watchful at zh_center
    narrator "屋簷之外，白影停在月光照不到的地方。"

    narrator "棉帽低低垂著，其下數點陰森的光微微轉動。"

    narrator "她像是在確認剛才那些身體說出的話，也像是在學習人的表情。"

    narrator "袖口深處，有什麼極細的東西輕輕縮了回去。"

    narrator "她沒有失望。"

    narrator "只是換了一種尋找的方法。"

    scene bg inn_room_late
    with dissolve

    narrator "他坐到天快亮。"

    narrator "腦中反覆的是同一個問題：他到底能保住多少人，又會失去誰。"

    show jingzhe wary at zh_center
    narrator "他沒有追問。"

    narrator "但他知道，有人正在用她們接近他。"

    narrator "而那個人，極可能就在月下庄附近。"

    narrator "至於真正的目的——"

    narrator "他還沒完全摸清。"

    jump chapter_6
label chapter_6:
    scene bg inn_morning
    with dissolve

    narrator "清晨的風比前幾天更乾。"

    narrator "像是雨季尚未來臨，卻已經開始預告。"

    show jingzhe stern at zh_center
    narrator "驚蟄站在後院，指尖捏著一撮未點燃的香。"

    jingzhe "……"

    narrator "他知道自己不能再只是等。"

    narrator "等下去，就會有人被帶走。"

    scene bg inn_kitchen
    with dissolve

    show hanami concerned at zh_far_left
    hanami "你今天看起來精神多了。"

    show jingzhe neutral at zh_center
    jingzhe "嗯。"

    show yumemi worried at zh_far_right
    yumemi "還有哪裡不舒服嗎？"

    jingzhe "沒有。"

    narrator "夢見的眼神依舊柔軟，但他注意到她會下意識避開某些角落。"

    narrator "像是那裡還殘著她不敢再看的東西。"

    scene bg inn_corridor_day
    with dissolve

    narrator "午後，他走到走廊盡頭，看見一點被踩過的灰。"

    narrator "灰裡混著極細的殼，像是小蜘蛛的遺骸。"

    show jingzhe stern at zh_center
    narrator "他沒有驚動別人，只是把灰掃進掌心。"

    narrator "那一刻，他明白了。"

    narrator "控制她們的，不只是人。"

    narrator "而他不能再假裝自己能置身事外。"

    scene bg inn_room_evening
    with dissolve

    narrator "入夜前，他在桌上攤開筆記。"

    narrator "不是小說，而是簡單的地圖。"

    narrator "月下庄、附近林道、能躲藏的洞窟與斷崖。"

    narrator "他把幾條路線畫得很慢。"

    show jingzhe pensive at zh_center
    narrator "那不是猶豫，而是他在逼自己確定。"

    narrator "每一條線，都像在計算他可能失去的人。"

    narrator "畫完後，他把郵箱收進房梁的暗格。"

    narrator "又用淡淡的蟲香封住氣味，像是把訊號埋進霧裡。"

    scene bg inn_hall_evening
    with dissolve

    show hanami concerned at zh_far_left
    hanami "你今天一直在想事情。"

    show jingzhe stern at zh_center
    jingzhe "……有事。"

    narrator "他終於開口。"

    narrator "沉默太久，就像一種背叛。"

    jingzhe "月底前，會有東西來。"

    hanami "什麼？"

    jingzhe "我不知道名字，但我知道牠們想找我。"

    show yumemi worried at zh_far_right
    yumemi "那我們怎麼辦？"

    narrator "驚蟄看著她們。"

    narrator "他本來想說『離開』。"

    narrator "但他知道，她們不會走。"

    narrator "而他也不想再被迫選擇犧牲誰。"

    jingzhe "我會阻止牠們。"

    show hanami determined at zh_far_left
    hanami "我跟你去。"

    narrator "花見的語氣沒有討論餘地。"

    narrator "她的眼神像已經把那條路先走完一遍。"

    jingzhe "……"

    narrator "她轉身回房，取出暮春大姊留下的薙刀。"

    show yumemi determined at zh_far_right
    yumemi "那……我守著月下庄。"

    jingzhe "好。"

    narrator "他點頭。"

    narrator "但袖口中那張黑色卡片，似乎有意識地貼上了指尖。"

    narrator "卡片很冷，像是早已等著他把某個人推向安全的那一邊。"

    narrator "而另一邊，則必須由他自己去承擔。"

    narrator "那一刻，他已經選好了路。"

    jump chapter_7_choice_1
label chapter_7_choice_1:
    $ first_route = None
    $ second_route = None

    menu:
        "把卡片交給誰？"

        "交給花見":
            $ first_route = "hanami"
            jump chapter_7_hanami_1

        "交給夢見":
            $ first_route = "yumemi"
            jump chapter_7_yumemi_1

label chapter_7_hanami_1:
    scene bg inn_hall_evening
    with dissolve

    narrator "驚蟄從袖中取出那張黑色卡片，交到花見手裡。"

    show jingzhe stern at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show hanami concerned at zh_far_left
    hanami "只保護我？"

    jingzhe "嗯。"

    show yumemi worried at zh_far_right
    yumemi "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    jingzhe "我會想辦法。"

    narrator "花見嘆了口氣，接著把卡片收進衣內，像是收下一種承諾。"
    show hanami determined at zh_far_left

    hanami "我會保管好。"


    narrator "驚蟄沒有再多看，轉身走向夜色。"

    narrator "他不想讓自己猶豫。"

    scene bg forest_path_night
    with fade

    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    narrator "他吹起煙草。"

    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    show hanami battle at zh_right
    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "是同伴。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙手如鐮。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_mid
    show hanami battle at zh_battle_party_right
    narrator "土蜘蛛先現身，像一堵牆，從樹影中慢慢逼近。"

    narrator "牠每一步都讓地面微震，像在逼近判決。"

    narrator "髮切先衝上去，鐮刃交錯，逼得牠抬頭防守。"

    narrator "牠的節肢拍地，揚起一層灰。"

    narrator "大百足自側面猛撞，震得地面一沉。"

    show hanami battle at zh_battle_party_right
    narrator "花見趁空隙切入，薙刀的刃光在牠的節肢上割出白痕。"

    narrator "她的呼吸短促，卻不退。"

    narrator "驚蟄的蟲影纏住牠的視線，逼得土蜘蛛退到樹根間。"

    scene bg inn_exterior_night
    with dissolve

    narrator "另一邊，月下庄靜得像沒有住人。"

    show jorogumo searching at zh_center
    narrator "絡新婦無聲地穿過屋簷，在屋內搜尋。"

    narrator "抽屜被拉開，又被無聲地推回原處。"

    narrator "桌下、床底、櫃後，凡是能藏東西的地方，都被她一一確認過。"

    narrator "沒有。"

    narrator "絡新婦停在房中央，指尖仍按著櫃門的邊緣。"

    narrator "她像是不信，又重新翻了一遍。"

    narrator "同樣的位置，同樣的空無。"

    narrator "那份從容終於在沉默裡裂開一線。"

    narrator "木框被推回去時，發出一聲很輕的悶響。"

    scene bg inn_corridor_night
    with fade

    show yumemi worried at zh_center
    narrator "夢見提著燈走出房門。"

    narrator "她望向走廊盡頭，低聲問了一句。"

    yumemi "誰在那裡？"

    narrator "沒有人回答。"

    narrator "只有一道細影，從梁上掠過。"

    scene bg inn_room_night
    with dissolve

    show yumemi frightened at zh_left
    narrator "夢見還來不及退後，燈火便猛地一晃。"

    show jorogumo attack at zh_right
    narrator "絡新婦將她拖進房裡，手掌覆住她的口鼻。"

    narrator "夢見的指尖抓住她的手腕，細微地掙動著。"

    narrator "絡新婦貼近她，聲音低得像絲線勒進耳中。"

    narrator "『郵箱在哪？』"

    narrator "夢見睜大眼睛，艱難地搖了搖頭。"

    narrator "那一瞬間，絡新婦眼底最後一點耐性也沉了下去。"
    show jorogumo enraged at zh_right

    narrator "她不是來空手而回的。"

    narrator "更不是來被一個無關緊要的人撞見的。"

    narrator "夢見像是想喊出花見的名字。"

    narrator "但聲音還沒成形，就被截斷了。"

    narrator "燈盞落在地上，火光晃了晃，沒有翻倒。"

    narrator "夢見倒下時，幾乎沒有發出聲音。"

    narrator "屋裡很安靜，像是什麼都沒有發生。"

    scene bg forest_path_night
    with dissolve

    narrator "土蜘蛛終於倒下。"

    narrator "花見喘著氣，髮絲黏在臉側。"

    show hanami concerned at zh_center
    hanami "回去吧……我很擔心夢見。"

    narrator "她的聲音發抖，像是早就知道會出事。"

    scene bg inn_gate_night
    with fade

    narrator "他們趕回月下庄。"

    show jorogumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_mid
    show hanami battle at zh_battle_party_right
    narrator "門口的影子還沒散，絡新婦正要退走。"

    narrator "花見的動作很大，很急，像把所有痛都甩出去。"

    narrator "驚蟄的蟲影從側面纏住她的腳。"

    narrator "一息之間，黑影碎成兩半。"

    narrator "那一瞬間，他們都明白了。"

    narrator "夢見——恐怕已經出事。"

    scene bg inn_hall_night
    with dissolve

    narrator "他們衝進屋裡。"

    narrator "看到的是夢見的身體。"

    show hanami grief at zh_left
    narrator "花見跪在地上，像被抽走了骨頭。"

    narrator "她的肩開始發抖，像在用力把聲音吞回去。"

    show jingzhe grief at zh_right
    narrator "驚蟄沒有安慰。"

    narrator "他知道，說什麼都沒用。"

    narrator "但他仍然把手放在她背上，短短一秒。"

    narrator "那一秒像是在告訴她：我在。"

    narrator "他把卡片從花見身上取回。"

    show jingzhe stern at zh_right
    narrator "撕開。"

    narrator "風停了一瞬。"

    narrator "他聽見了耳語，像從很遠的地方飄來。"

    narrator "「再做一次選擇。」"

    narrator "他閉上眼。"

    $ second_route = "yumemi"
    jump chapter_7_transition_second
label chapter_7_yumemi_1:
    scene bg inn_hall_evening
    with dissolve

    narrator "驚蟄從袖中取出那張黑色卡片，交到夢見手裡。"

    show jingzhe stern at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show yumemi worried at zh_far_right
    yumemi "只保護我……嗎？"

    jingzhe "嗯。"

    show hanami concerned at zh_far_left
    hanami "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    jingzhe "我會想辦法。"

    show yumemi determined at zh_far_right
    yumemi "我會小心的。"

    narrator "她把卡片收進衣內，像是抱著一件不能說的祕密。"

    show jingzhe wary at zh_center
    narrator "驚蟄看著她的手指收緊，又鬆開。"

    narrator "那一瞬間，他差點想把卡抽回來。"

    narrator "但他知道，猶豫會把人推向更壞的選項。"

    narrator "他轉身走向夜色。"

    scene bg forest_path_night
    with fade

    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    narrator "他吹起煙草。"

    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    show hanami battle at zh_right
    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "自己人。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙手如鐮。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_mid
    show hanami battle at zh_battle_party_right
    narrator "土蜘蛛先現身，像一座移動的山。"

    narrator "牠的影子蓋下來時，連空氣都變重。"

    narrator "髮切牽住牠的正面，大百足自側面猛撞。"

    show hanami battle at zh_battle_party_right
    narrator "花見握緊薙刀，步伐大開大合。"

    narrator "她的攻勢猛烈，卻也留下空隙。"

    narrator "驚蟄看見了——也來不及提醒。"

    narrator "絡新婦就在那道空隙裡出現。"

    scene bg forest_path_night
    with dissolve

    show jorogumo attack at zh_left
    narrator "一抹細影掠過花見的肩。"

    narrator "像蜘蛛絲輕輕擦過皮膚，連痛都來得很晚。"

    show hanami injured at zh_right
    narrator "花見的身體晃了一下，像被拉住了線。"

    narrator "她咬住一聲喘息，還想把薙刀舉回原位。"

    narrator "驚蟄想回頭，卻被土蜘蛛逼住。"

    narrator "牠的節肢拍地，揚起一層灰，把視線切碎。"

    narrator "他只能把那一瞬間記在心裡。"

    narrator "最後，土蜘蛛倒下。"

    narrator "土蜘蛛倒下的瞬間，絡新婦的影子已經往樹梢更深處退。"

    jingzhe "……別想走。"

    narrator "髮切像被放出的刀光，追著那道細影竄上去。"

    narrator "鐮刃一閃，黑影斷成幾截，落地時只剩一圈散開的絲。"

    narrator "驚蟄沒有立刻鬆一口氣。"

    narrator "他第一個想到的不是勝利，而是：太安靜了。"

    scene bg forest_path_night
    with dissolve

    show hanami injured at zh_center
    narrator "花見倒下的聲音很輕。"

    narrator "輕得像不該發生。"

    show jingzhe grief at zh_right
    narrator "驚蟄回頭的瞬間，胸口像被敲了一下。"

    narrator "他蹲下身，手指碰到她的頸側。"

    narrator "雨水很冷。"

    narrator "那裡更冷。"

    jingzhe "……花見。"

    narrator "他沒有多說，只把外衣蓋到她肩上。"

    narrator "然後，他把她抱起來。"

    narrator "動作很穩，像是怕一鬆手，她就會被夜色帶走。"

    scene bg forest_path_night
    with fade

    narrator "回月下庄的路比想像中更長。"

    narrator "他抱著她走，木屐聲被雨吞得很低。"

    scene bg inn_gate_night
    with dissolve

    narrator "月下庄的門口亮著燈。"

    show yumemi grief at zh_center
    narrator "夢見站在門邊，臉上全是雨。"

    narrator "她看見驚蟄懷裡的人時，整個人僵住。"

    yumemi "姐……姐？"

    narrator "驚蟄沒有回答。"

    narrator "他只是把視線移開，像是不敢多看那雙眼睛。"

    scene bg inn_hall_night
    with dissolve

    narrator "他把花見放在榻榻米上。"

    narrator "那一刻，夢見的聲音才真正從喉間掉出來。"

    show yumemi grief at zh_left
    narrator "她跪下去，像是被抽走了力氣。"

    show jingzhe grief at zh_right
    narrator "驚蟄站在旁邊，手掌還留著她的重量。"

    narrator "他想說什麼，卻一句也擠不出來。"

    jingzhe "把卡給我。"

    narrator "夢見抖著手，把卡片遞出去。"

    narrator "驚蟄接過時，指節白得發青。"

    narrator "撕開。"

    narrator "風停了一瞬。"

    narrator "他聽見了耳語，像從很遠的地方飄來。"

    narrator "「再做一次選擇。」"

    narrator "雨聲被掐斷。"

    narrator "他閉上眼。"

    $ second_route = "hanami"
    jump chapter_7_transition_second
label chapter_7_transition_second:
    scene black
    with fade

    centered "記憶像一層薄霧倒流。\n\n你被迫回到交出卡片之前的那一刻。"

    if second_route == "hanami":
        jump chapter_7_hanami_2
    else:
        jump chapter_7_yumemi_2

label chapter_7_hanami_2:
    scene bg inn_hall_evening
    with dissolve

    narrator "驚蟄從袖中取出那張黑色卡片，交到花見手裡。"

    show jingzhe wary at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show hanami concerned at zh_far_left
    hanami "只保護我？"

    jingzhe "嗯。"

    show yumemi worried at zh_far_right
    yumemi "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    narrator "明明只是同樣的問題，他胸口卻像被什麼輕輕拽了一下。"

    jingzhe "我會想辦法。"

    hanami "你講這種話的時候，最不可信。"

    narrator "她低聲說完，還是把卡片收進衣內，像是收下一種承諾。"

    hanami "我會保管好。"

    show jingzhe grief at zh_center
    narrator "驚蟄盯著那個動作。"

    narrator "他說不出原因。"

    narrator "可心口那一下抽緊太真，真得像他已經為這個動作後悔過一次。"

    narrator "只是覺得——這張卡不該離開他的手。"

    jingzhe "……拿好。別逞強。"

    narrator "話出口的瞬間，他自己都愣了一下。"

    narrator "他平常不會用這種語氣說話。"

    narrator "像是有一段不屬於此刻的記憶，正隔著薄霧貼在他皮膚上。"

    narrator "他不去抓那霧裡的畫面，只把煙斗握緊。"

    scene bg forest_path_night
    with fade

    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    narrator "他吹起煙草。"

    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    show hanami battle at zh_right
    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "是同伴。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙手如鐮。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_mid
    show hanami battle at zh_battle_party_right
    narrator "土蜘蛛先現身，像一堵牆，從樹影中慢慢逼近。"

    narrator "牠每一步都讓地面微震，像在逼近判決。"

    narrator "髮切先衝上去，鐮刃交錯，逼得牠抬頭防守。"

    narrator "牠的節肢拍地，揚起一層灰。"

    narrator "大百足自側面猛撞，震得地面一沉。"

    show hanami battle at zh_battle_party_right
    narrator "花見趁空隙切入，薙刀的刃光在牠的節肢上割出白痕。"

    narrator "驚蟄下意識往前一步，像要把她往後推。"

    jingzhe "別太前——"

    narrator "他只說出半句。"

    narrator "花見沒有回頭，卻像聽懂了。"

    narrator "她的步伐稍微收了一點，依舊不退。"

    narrator "驚蟄的蟲影纏住牠的視線，逼得土蜘蛛退到樹根間。"

    scene bg inn_exterior_night
    with dissolve

    narrator "另一邊，月下庄靜得像沒有住人。"

    show jorogumo searching at zh_center
    narrator "絡新婦無聲地穿過屋簷，在屋內搜尋。"

    narrator "抽屜被拉開，又被無聲地推回原處。"

    narrator "桌下、床底、櫃後，凡是能藏東西的地方，都被她一一確認過。"

    narrator "沒有。"

    narrator "絡新婦停在房中央，指尖仍按著櫃門的邊緣。"

    narrator "她像是不信，又重新翻了一遍。"

    narrator "同樣的位置，同樣的空無。"

    narrator "那份從容終於在沉默裡裂開一線。"

    narrator "木框被推回去時，發出一聲很輕的悶響。"

    scene bg inn_corridor_night
    with fade

    show yumemi worried at zh_center
    narrator "夢見提著燈走出房門。"

    narrator "她望向走廊盡頭，低聲問了一句。"

    yumemi "誰在那裡？"

    narrator "沒有人回答。"

    narrator "只有一道細影，從梁上掠過。"

    scene bg inn_room_night
    with dissolve

    show yumemi frightened at zh_left
    narrator "夢見還來不及退後，燈火便猛地一晃。"

    show jorogumo attack at zh_right
    narrator "絡新婦將她拖進房裡，手掌覆住她的口鼻。"

    narrator "夢見的指尖抓住她的手腕，細微地掙動著。"

    narrator "絡新婦貼近她，聲音低得像絲線勒進耳中。"

    narrator "『郵箱在哪？』"

    narrator "夢見睜大眼睛，艱難地搖了搖頭。"

    narrator "那一瞬間，絡新婦眼底最後一點耐性也沉了下去。"
    show jorogumo enraged at zh_right

    narrator "她不是來空手而回的。"

    narrator "更不是來被一個無關緊要的人撞見的。"

    narrator "夢見像是想喊出花見的名字。"

    narrator "但聲音還沒成形，就被截斷了。"

    narrator "燈盞落在地上，火光晃了晃，沒有翻倒。"

    narrator "夢見倒下時，幾乎沒有發出聲音。"

    narrator "屋裡很安靜，像是什麼都沒有發生。"

    scene bg forest_path_night
    with dissolve

    narrator "土蜘蛛終於倒下。"

    narrator "花見喘著氣，髮絲黏在臉側。"

    show hanami concerned at zh_center
    hanami "回去吧……我很擔心夢見。"

    narrator "她的聲音發抖，像是早就知道會出事。"

    narrator "驚蟄的胸口那股莫名的拉扯又更重了一點。"

    scene bg inn_gate_night
    with fade

    narrator "他們趕回月下庄。"

    show jorogumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_mid
    show hanami battle at zh_battle_party_right
    narrator "門口的影子還沒散，絡新婦正要退走。"

    narrator "驚蟄甚至沒有讓花見先動。"

    jingzhe "這次不會。"

    narrator "他的蟲影先一步纏住黑影的退路。"

    narrator "花見的薙刀落下，乾淨得像切斷一根線。"

    narrator "黑影碎成兩半。"

    narrator "那一瞬間，他們都明白了。"

    narrator "夢見——恐怕已經出事。"

    scene bg inn_hall_night
    with dissolve

    narrator "他們衝進屋裡。"

    narrator "可還沒看清屋內，驚蟄的指尖就先發了冷。"

    narrator "像是那個結局早一步沿著骨頭爬了回來。"

    narrator "看到的是夢見的身體。"

    show hanami grief at zh_left
    narrator "花見跪在地上，像被抽走了骨頭。"

    narrator "她的肩開始發抖，像在用力把聲音吞回去。"

    show jingzhe grief at zh_right
    narrator "驚蟄伸手去扶她，手卻在半空停住。"

    narrator "他忽然想起自己曾經抱著一個人走過雨。"

    narrator "那個重量、那個冷，像是刻在掌心。"

    narrator "那股記憶來得太真，他忍不住低低吐出一口氣。"

    jingzhe "……夠了。"

    narrator "像是在對誰說，又像是在對自己。"

    narrator "他把手放在花見背上，這次沒有只停一秒。"

    narrator "他把卡片從花見身上取回。"

    show jingzhe stern at zh_right
    narrator "撕開。"

    narrator "風停了一瞬。"

    narrator "他聽見了耳語，像從很遠的地方飄來。"

    narrator "「再做一次選擇。」"

    narrator "他閉上眼。"

    jump chapter_8_choice
label chapter_7_yumemi_2:
    scene bg inn_hall_evening
    with dissolve

    narrator "驚蟄從袖中取出那張黑色卡片，交到夢見手裡。"

    show jingzhe wary at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show yumemi worried at zh_far_right
    yumemi "只保護我……嗎？"

    jingzhe "嗯。"

    show hanami concerned at zh_far_left
    hanami "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    narrator "明明只是同樣的問題，他卻覺得指節在發冷。"

    jingzhe "我會想辦法。"

    show yumemi determined at zh_far_right
    yumemi "我會小心的。"

    narrator "她把卡片收進衣內，像是抱著一件不能說的祕密。"

    show jingzhe grief at zh_center
    narrator "驚蟄看著她的手指收緊，又鬆開。"

    narrator "像是有一段不屬於此刻的記憶，正隔著薄霧貼在他皮膚上。"

    narrator "他不去想那霧裡是什麼。"

    narrator "可指尖還是先一步收緊，像身體比他更早記得失去是什麼。"

    narrator "那一瞬間，他差點想把卡抽回來。"

    narrator "但他知道，猶豫會把人推向更壞的選項。"

    narrator "他轉身走向夜色。"

    scene bg forest_path_night
    with fade

    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    narrator "他吹起煙草。"

    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    show hanami battle at zh_right
    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "自己人。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙手如鐮。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_mid
    show hanami battle at zh_battle_party_right
    narrator "土蜘蛛先現身，像一座移動的山。"

    narrator "牠的影子蓋下來時，連空氣都變重。"

    narrator "髮切牽住牠的正面，大百足自側面猛撞。"

    show hanami battle at zh_battle_party_right
    narrator "花見握緊薙刀，步伐大開大合。"

    narrator "她的攻勢猛烈，卻也留下空隙。"

    narrator "驚蟄看見了——也來不及提醒。"

    narrator "他甚至有一瞬間覺得：自己早就知道會發生什麼。"

    narrator "那種預感太真，像是有人把答案塞進他舌根底下。"

    narrator "絡新婦就在那道空隙裡出現。"

    scene bg forest_path_night
    with dissolve

    show jorogumo attack at zh_left
    narrator "一抹細影掠過花見的肩。"

    narrator "像蜘蛛絲輕輕擦過皮膚，連痛都來得很晚。"

    show hanami injured at zh_right
    narrator "花見的身體晃了一下，像被拉住了線。"

    narrator "她咬住一聲喘息，還想把薙刀舉回原位。"

    narrator "驚蟄想回頭，卻被土蜘蛛逼住。"

    narrator "牠的節肢拍地，揚起一層灰，把視線切碎。"

    narrator "他只能把那一瞬間記在心裡。"

    narrator "最後，土蜘蛛倒下。"

    narrator "土蜘蛛倒下的瞬間，絡新婦的影子已經往樹梢更深處退。"

    jingzhe "……別想走。"

    narrator "髮切像被放出的刀光，追著那道細影竄上去。"

    narrator "鐮刃一閃，黑影斷成幾截，落地時只剩一圈散開的絲。"

    narrator "驚蟄沒有立刻鬆一口氣。"

    narrator "他第一個想到的不是勝利，而是：太安靜了。"

    narrator "那種安靜像曾經貼著他的耳骨，冷得讓人來不及回頭。"

    narrator "他甚至還沒看見花見倒下，胸口就先沉了下去。"

    scene bg forest_path_night
    with dissolve

    narrator "驚蟄轉身回頭。"

    narrator "他不喜歡回頭。"

    narrator "但這次，他幾乎是衝過去的。"

    show hanami injured at zh_center
    narrator "花見倒在濕冷的落葉上，薙刀躺在她指尖不遠處。"

    show jingzhe grief at zh_right
    narrator "驚蟄蹲下身，手指碰到她的頸側。"

    narrator "那裡很冷。"

    jingzhe "花見……"

    narrator "他的聲音破了一下，像是他自己也沒預料到。"

    narrator "他把外衣蓋到她肩上，又替她把臉側的雨抹開。"

    narrator "指尖在顫。"

    narrator "他深吸一口氣，硬把那點顫抹平。"

    narrator "然後，他把她抱起來。"

    narrator "動作很輕，像是怕驚動她。"

    scene bg forest_path_night
    with fade

    narrator "回月下庄的路比想像中更長。"

    narrator "雨打在他手背上，冷得像提醒。"

    narrator "他抱得更緊了一點。"

    scene bg inn_gate_night
    with dissolve

    narrator "月下庄的門口亮著燈。"

    show yumemi grief at zh_center
    narrator "夢見站在門邊，像是等了很久。"

    narrator "她看見驚蟄懷裡的人時，整個人僵住。"

    narrator "燈光在她眼裡碎成一片。"

    yumemi "姐……姐？"

    narrator "驚蟄沒有回答。"

    narrator "他只是把視線移開，像是不敢多看那雙眼睛。"

    scene bg inn_hall_night
    with dissolve

    narrator "他把花見放在榻榻米上。"

    narrator "那一刻，夢見的聲音才真正從喉間掉出來。"

    show yumemi grief at zh_left
    narrator "她跪下去，像是被抽走了力氣。"

    show jingzhe grief at zh_right
    narrator "驚蟄站在旁邊，手掌還留著她的重量。"

    narrator "他想說『對不起』，卻發不出聲。"

    narrator "最後只低低說了一句。"

    jingzhe "把卡給我。"

    narrator "夢見抖著手，把卡片遞出去。"

    narrator "驚蟄接過時，指節白得發青。"

    narrator "撕開。"

    narrator "風停了一瞬。"

    narrator "他聽見了耳語，像從很遠的地方飄來。"

    narrator "「再做一次選擇。」"

    narrator "雨聲被掐斷。"

    narrator "他閉上眼。"

    jump chapter_8_choice
label chapter_8_choice:
    scene bg inn_hall_evening
    with dissolve

    narrator "同樣的走廊，同樣的燈。"

    narrator "同樣的呼吸聲。"

    show jingzhe grief at zh_center
    narrator "驚蟄站在原地，手裡握著那張全黑的卡片。"

    narrator "他沒有立刻看花見，也沒有看夢見。"

    narrator "因為他知道，只要視線一偏，就會再次被拖進某個結局。"

    narrator "耳邊有聲音，像灰裡的火。"

    narrator "『再選一次。』"

    narrator "他聽過了。"

    narrator "也受夠了。"


    menu:
        "這次要怎麼做？"

        "把卡留給自己":
            jump chapter_8_true_end
label chapter_8_true_end:
    show hanami concerned at zh_far_left
    hanami "怎麼了？你臉色很差。"

    show yumemi worried at zh_far_right
    yumemi "驚蟄先生……你還好嗎？"

    narrator "驚蟄低頭，看著手裡的卡。"

    narrator "它很輕。"

    narrator "卻像能壓垮一整個三月。"

    jingzhe "……這次不選你們。"
    show jingzhe stern at zh_center

    show hanami surprised at zh_far_left
    hanami "欸？什麼意思？"

    show yumemi worried at zh_far_right
    yumemi "是那、那張卡嗎？"

    narrator "他把卡收進袖口，像把一把刀藏回鞘裡。"

    jingzhe "卡我自己留著。"

    jingzhe "你們留在月下庄。"

    show hanami determined at zh_far_left
    hanami "不行。我說了我跟你去。"

    show jingzhe stern at zh_center
    narrator "驚蟄的視線終於落到花見身上。"

    narrator "他很想說『別逞強』。"

    narrator "卻又覺得自己沒有資格。"

    jingzhe "這不是逞強。"

    jingzhe "是分工。"

    narrator "他說得很冷。"

    narrator "冷到連自己都覺得像是在推開人。"

    show yumemi worried at zh_far_right
    yumemi "可是……我們也可以一起……"

    jingzhe "不。"

    narrator "他拒絕得太快。"

    narrator "像是如果慢一拍，就會被某段記憶拖走。"

    narrator "他沒有解釋他看見了什麼。"

    narrator "他只知道："

    narrator "這一次，他要把結局留在自己身上。"

    show hanami angry at zh_far_left
    hanami "你把我當什麼？"

    jingzhe "……我把你當活著的人。"

    narrator "花見的怒氣卡在喉間。"

    narrator "她握著薙刀的手緊了一下，又鬆開。"

    show yumemi determined at zh_far_right
    yumemi "那我做什麼？"

    jingzhe "守門。"

    narrator "驚蟄看向夢見。"

    narrator "那雙眼睛太溫柔，溫柔到讓人想逃。"

    jingzhe "如果有任何不對勁，就把窗打開。"

    jingzhe "讓風進來。"

    narrator "他沒有說『讓我聞得到』。"

    narrator "但她們都懂，那句話背後是什麼。"

    show hanami determined at zh_far_left
    hanami "那你呢？"

    jingzhe "我去把牠們的月底，提前到今晚。"

    narrator "他轉身前停了一下。"

    show jingzhe softened at zh_center
    jingzhe "……我袖口那張卡。"

    jingzhe "把卡片給他的人只說過一句：撕開會保護持有它的人。"

    jingzhe "我不知道它到底怎麼保護。"

    jingzhe "但我知道一件事——別碰它。"

    show hanami surprised at zh_far_left
    hanami "那你為什麼還帶著？"

    jingzhe "因為我不想再把命交給它替我選。"

    narrator "他沒有把『也不想再看你們死』說出口。"

    scene bg inn_room_night
    with fade

    narrator "回到房裡，他把郵箱從暗格取出，又放回去。"

    narrator "他在門上留了淡淡的蟲香。"

    narrator "不是用來召喚，而是用來遮蔽。"

    show jingzhe pensive at zh_center
    narrator "他點燃煙斗。"
    show jingzhe smoking at zh_center

    narrator "這次燃的不是平常那種。"

    narrator "味道更苦，更沉，像是把夜色咬碎。"

    narrator "這種香會讓髮切與大百足變得更兇、更快。"

    narrator "代價是毒性。"

    narrator "第一口下去，他就覺得喉嚨像被砂紙磨過。"

    narrator "第二口開始，胸腔會慢半拍，像心臟被人用指尖按住。"

    narrator "他知道自己會變慢。"

    narrator "只是他選擇把那個『慢』留給自己。"

    narrator "髮切與大百足在陰影裡醒來。"

    show jingzhe battle at zh_center
    jingzhe "走。"

    scene bg forest_path_night
    with dissolve

    narrator "林道的黑像一盆水。"

    narrator "他踏進去時，連呼吸都被濕度磨鈍。"

    narrator "他知道牠們在等。"

    narrator "也知道，這次只有他。"

    scene bg forest_clearing_night
    with fade

    show tsuchigumo attack at zh_left
    narrator "土蜘蛛先現身。"

    narrator "牠的身影像一座移動的丘，沉得讓樹枝都不敢搖。"

    show jorogumo watchful at zh_right
    narrator "絡新婦沒有立刻現形。"

    narrator "她藏在更高的地方，像一根看不見的線。"

    show tsuchigumo attack at zh_battle_monster_left
    show jorogumo watchful at zh_monster_cluster_mid
    show jingzhe battle at zh_battle_party_right
    narrator "驚蟄吐出一口煙。"

    narrator "髮切的鐮光先到。"

    narrator "比平常更快，更狠，像貼著他的呼吸在切。"

    narrator "大百足的撞擊緊跟其後。"

    narrator "土蜘蛛迎上來，節肢拍地，震得泥土翻起。"

    narrator "他不退。"

    narrator "因為退一步，後面就會有人死。"

    narrator "他聞到了那股細尖的味道。"

    narrator "絡新婦在移動。"

    jingzhe "……在上面。"

    narrator "他沒有抬頭。"

    narrator "抬頭就會露出喉嚨。"

    narrator "他把煙斗轉了個角度。"

    narrator "香味變了。"

    narrator "髮切忽然一折，像聽見了另一個命令，鐮刃往樹梢一掃。"

    show jorogumo attack at zh_monster_cluster_mid
    narrator "黑影被逼出半寸。"

    narrator "絡新婦的身形在月光裡顫了一下。"

    narrator "她笑。"

    narrator "那笑聲沒有溫度。"

    narrator "然後，她消失。"

    narrator "下一瞬，細影已經在他背後。"

    show jingzhe injured at zh_battle_party_right
    narrator "驚蟄的肩一沉。"

    narrator "像被絲線套住。"

    narrator "他咬住一口氣，沒讓自己發出聲音。"

    narrator "大百足猛地回身，把那道影子撞開。"

    narrator "他趁空隙把煙吸進肺裡。"

    narrator "苦到像把人拉回現實。"

    narrator "土蜘蛛趁機衝撞。"

    narrator "他被逼退半步。"

    narrator "腳跟踩到一塊濕滑的石。"

    narrator "那一瞬間，他第一次感覺到："

    narrator "自己可能會死。"

    jingzhe "……很好。"

    narrator "他說得很輕。"

    narrator "像是在說服誰。"

    narrator "他把香捏碎。"

    narrator "味道陡然變烈。"

    narrator "髮切的鐮刃刺入土蜘蛛節肢的縫。"

    narrator "大百足用整個身軀壓上去。"

    narrator "土蜘蛛的嘶聲像碎木。"

    narrator "牠倒下時，地面像沉了一口氣。"
    hide tsuchigumo

    narrator "髮切與大百足像還沒盡興，氣息比剛才更兇。"

    narrator "代價也同時回到驚蟄身上。"

    narrator "他吐出一口煙，胸口卻像被撕開一條細縫。"

    narrator "但驚蟄沒有鬆一口氣。"

    narrator "因為最陰的那一隻還在。"

    narrator "絡新婦。"

    narrator "他聞到她靠近。"

    narrator "比剛才更快。"

    narrator "他轉身，煙斗的火光像一點星。"

    show jorogumo enraged at zh_right
    narrator "絡新婦終於現形。"

    narrator "她的指尖像要去拿走他袖口裡的卡。"

    narrator "驚蟄本能地想閃。"

    narrator "但毒性讓他的身體慢了半拍。"

    show jingzhe injured at zh_center
    narrator "他抬手擋住，卻只來得及擋掉一半。"

    narrator "另一半落在他的肋側。"

    narrator "鈍痛先到，溫熱才跟上。"

    narrator "他聽見自己呼吸裡有一聲很輕的破裂。"

    narrator "那一下讓他的手腕也發出一聲鈍響。"

    narrator "痛像白光。"

    narrator "他沒有退。"

    narrator "他吐出最後一口煙。"

    narrator "髮切從她側面切入。"

    narrator "黑影碎開，像被剪斷的絲。"

    narrator "絡新婦倒下時，還在笑。"

    narrator "像是在說：你以為這樣就結束了嗎？"
    hide jorogumo

    narrator "驚蟄跪下去。"

    narrator "膝蓋撞到石頭，痛得他眼前發黑。"

    narrator "他摸到自己的肋側。"

    narrator "溫熱的東西正在流。"

    narrator "他想起那張卡。"

    narrator "『會保護持有它的人。』"

    narrator "他笑了一下。"

    jingzhe "……騙子。"

    scene bg forest_clearing_night
    with dissolve

    show jingzhe injured at zh_center
    narrator "遠處有腳步聲。"

    narrator "兩道。"

    show hanami tearful at zh_left
    narrator "花見的聲音先到。"

    hanami "驚蟄！"

    show yumemi tearful at zh_right
    narrator "夢見跟在後面，喘得很急。"

    yumemi "你、你怎麼可以一個人……"

    narrator "驚蟄想說『回去』。"

    narrator "嘴唇卻只吐出一點氣。"

    show hanami tearful at zh_left
    narrator "花見看到他身上的血時，臉色瞬間白了。"

    narrator "她伸手去摸他的袖口。"

    hanami "卡——！"

    narrator "她要撕。"

    show jingzhe injured at zh_center
    narrator "驚蟄抓住她的手腕。"

    jingzhe "不要。"

    narrator "他說得很慢。"

    narrator "慢到像是把每個音節都吞過一遍。"

    jingzhe "我不想再……選。"

    narrator "花見的眼睛紅得發亮。"

    hanami "你會死！"

    jingzhe "……我知道。"

    narrator "他抬眼看她。"

    narrator "那眼神沒有討好，也沒有求救。"

    narrator "只有一種終於停下來的疲倦。"

    jingzhe "這樣……就好。"

    narrator "夢見捂住嘴，像怕自己哭出聲就會把他推走。"

    show yumemi tearful at zh_right
    yumemi "可是我們……"

    jingzhe "你們活著。"

    narrator "他說完這句話，像把最後一口氣也交出去。"

    narrator "他靠著樹根，眼皮沉下來。"

    narrator "他聽見花見在罵。"

    narrator "聽見夢見在哭。"

    narrator "但那些聲音都像隔著水。"

    narrator "就在他準備把自己沉下去時——"

    narrator "卡片忽然變輕。"

    narrator "像是被誰抽走。"

    show jingzhe injured at zh_center
    narrator "驚蟄睜開一點眼。"

    narrator "黑色的卡片不見了。"

    jingzhe "……"

    narrator "下一瞬，夜色被撕開一條縫。"

    scene bg forest_clearing_night
    with flash

    show shadow_witch annoyed at zh_shadow_left
    show jingzhe injured at zh_party_cluster_left
    narrator "影之魔女站在那裡。"

    narrator "她的披風像夜本身。"

    narrator "她皺著眉，像在看一件很麻煩的事。"

    shadow_witch "我不是說過，別把卡片交給別人嗎。"

    narrator "驚蟄想笑。"

    narrator "卻咳出一口血。"

    shadow_witch "……真會添麻煩。"

    narrator "她的手指一點。"

    narrator "像按掉一盞燈。"

    narrator "痛忽然被抽走一半。"

    narrator "他的呼吸重新回到胸腔。"

    show shadow_witch annoyed at zh_shadow_left
    show jingzhe injured at zh_party_cluster_left
    show hanami surprised at zh_party_cluster_center
    hanami "你、你是——"

    show yumemi surprised at zh_party_cluster_right
    yumemi "影之……魔女……"

    shadow_witch "別靠近。"
    show shadow_witch cold at zh_shadow_left

    narrator "她說得很冷。"

    narrator "像是怕沾到什麼。"

    narrator "視線卻落在驚蟄身上。"

    shadow_witch "你也真敢。"
    show shadow_witch annoyed at zh_shadow_left

    jingzhe "……卡片沒有保護我。"

    narrator "他說得很平。"

    narrator "像抱怨一件日用品壞了。"

    shadow_witch "它保護的從來不是肉身。"
    show shadow_witch concerned at zh_shadow_left

    shadow_witch "是你把命運握回自己手裡的那一刻。"

    narrator "她把卡片收回袖中。"

    shadow_witch "受傷這種事，不在它的仁慈裡。"

    narrator "驚蟄閉上眼。"

    narrator "他忽然很想說一句話。"

    narrator "但他沒有。"

    narrator "因為他知道，她不需要。"

    shadow_witch "你寫的最新一章，我還沒收到。"

    narrator "那句話像針。"

    narrator "又像某種奇怪的溫柔。"

    jingzhe "……我會寫。"

    shadow_witch "最好。"
    show shadow_witch annoyed at zh_shadow_left

    narrator "她轉身，夜色跟著收束。"

    shadow_witch "還有。"

    narrator "她停了一下。"

    shadow_witch "別再讓我跑第二趟。"

    narrator "她消失得像沒來過。"

    scene bg forest_clearing_night
    with dissolve

    show jingzhe injured at zh_center
    narrator "風回來了。"

    narrator "雨也回來了。"

    show hanami tearful at zh_left
    narrator "花見的手顫著，終於敢去摸驚蟄的臉。"

    show yumemi tearful at zh_right
    narrator "夢見也靠近，像怕一眨眼他又會被帶走。"

    show jingzhe softened at zh_center
    narrator "驚蟄吸了一口氣。"

    narrator "這一次，他沒有把她們推開。"

    jingzhe "回去吧。"

    narrator "他說得很輕。"

    narrator "像把整個三月都放下。"

    scene bg inn_hall_night
    with fade

    narrator "月下庄的燈重新點起來。"

    narrator "三個人的影子靠得很近。"

    narrator "近得像只要誰先鬆手，今夜就會重新碎開。"

    narrator "可這一次，沒有人先放。"

    narrator "他們誰都沒有說今天結束了。"

    narrator "但他們都知道："

    narrator "至少，這次會一起走到明天。"


    scene bg inn_morning
    with dissolve

    narrator "清晨的風很淡。"

    narrator "像是昨夜從沒流過血。"

    narrator "只有桌上的煙斗，還留著一點苦味。"

    jump end_game
label end_game:
    scene black
    with fade

    return

