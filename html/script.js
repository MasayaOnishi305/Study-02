//var order_menu = order_menu.value;
var search_word = document.getElementById('search_word');
var search = document.getElementById('search');
var log = document.getElementById('log');
var csv_name = document.getElementById('csv_name');
var output = document.getElementById('output');

search.addEventListener('click', () => {
    //必須チェック
    if(search_word.value == ""){
        window . alert('検索ワードを入力してください' );
    }
    else{
        //ログの取得
        async function run() {
            let add_value = await eel.search(search_word.value);
        }
        run();
        
    }
});

output.addEventListener("click", () => {
    if (csv_name.value == ""){
        alert("csvが入力されていません");
        return false;
    }
    eel.csv_output(csv_name.value);
})

eel.expose(return_log)
function return_log(text) {
    log.value = text;
}

eel.expose(alertJs)
function alertJs(text){
    alert(text)
}

// eel.expose(view_log_js)
// function view_log_js(text){
//     var inputVal = text[0]+'\n';
//     log.value = (log.value+inputVal);
//     total.value = text[1];
//     storage.setItem('total_price',text[1]);
//     window . alert(storage.getItem('total_price'));
// }
//画面遷移処理
// function link(target) {
//     window.location.href=target;
// }
