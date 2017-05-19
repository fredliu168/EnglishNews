/**
 * Created by fred on 2017/5/16.
 */
new Vue({
    el: '#app',
    data: {
        visible: false,
        isOut:true,
        selected_word_elem: null,
        new_content: '', //新闻内容
        word_phonetic: '',
        word_explains: '',
        selected_word: "",
        bottom_box: null,
        api: '/api/v1.0/',
        new_image_url:'',
        newid:0
    },

    mounted: function () {

        this.newid = $("#newid").text();

        this.new_image_url = this.api+'image/'+this.newid+'.jpg';

        console.log(this.newid);

        this.getText(this.newid);

        // var p = $('p');
        //
        // p.html(function (index, oldHtml) {
        //     var htm = oldHtml.replace(/\b(\w+?)\b/g, '<span class="word">$1</span>');
        //     console.log(htm);
        //     return htm;
        // });


    },
    methods: {
        close: function () {
            console.log(this.selected_word_elem);
            this.selected_word_elem.className = "word";
            console.log("close");
        },

        setWordExplains: function () {
            var p = $('p');
            p.html(function (index, oldHtml) {
                var htm = oldHtml.replace(/\b(\w+?)\b/g, '<span class="word">$1</span>');
                console.log(htm);
                return htm;
            });
            this.bottom_box = $(".bottom_box");

            //var isOut = true;

            $(".close").click(function () {
                $(".bottom_box").hide();
            })

            var span = $('span');

            var vm = this;

            var other = window.document;

            other.onclick = function () {

                if (vm.isOut) {
                    $(".bottom_box").hide();
                    vm.isOut = false;
                }

                vm.isOut = true;

            }

            span.click(function (event) {

                vm.isOut = false;

                if (vm.selected_word_elem != null) {
                    vm.selected_word_elem.className = "word";
                }
                event.target.className = "word_selected";
                vm.selected_word_elem = event.target;
                vm.selected_word = event.target.innerHTML;
                vm.word_explains = '';
                vm.word_phonetic = '';
                //vm.visible = true;

                console.log(vm.selected_word);

                vm.bottom_box.show();

                //this.$message('这是一条消息提示');

                var url = vm.api + 'query/' + vm.selected_word;

                $request.get(url, null, function (data) {

                    console.log(data);
                    vm.word_phonetic = data['basic']['us-phonetic'];
                    vm.word_explains = data['basic']['explains'];

                    if(vm.word_phonetic != null)
                    {
                        vm.word_phonetic = '/'+vm.word_phonetic+'/';
                    }

                }, function (err_data) {

                })


            });

        },

        getText: function (newID) {

            var vm = this;
            var url = vm.api + 'news/' + newID;


            $request.get(url, null, function (data) {

                console.log(data);
                vm.new_content = data['data'];
                vm.$nextTick(function () {
                    //渲染完毕
                    console.log('渲染完毕');
                    vm.setWordExplains();//设置可以查单词

                });

            }, function (err_data) {

            })
        }


    }
})