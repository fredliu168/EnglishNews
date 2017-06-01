/**
 * Created by fred on 2017/5/16.
 */
new Vue({
    el: '#app',
    data: {
        loading: false,
        news_list: [], //新闻内容
        api: '/api/v1.0/',
        titleImage:'',
        titleNews:'',
        firstNew:{
            ReadCount:0,
            WordCount:0,
            HardWeight:0,
            Source:'',
            newid:0
        }

    },
    mounted: function () {
        this.loading = true;
        this.getList(0);
    },
    components: {
        'vue-pull-refresh': VuePullRefresh
    },
    methods: {
        getList: function (maxid) {

            var vm = this;
            var url = vm.api + 'news-list/' + maxid;

            $request.get(url, null, function (data) {

                console.log(data);
                vm.news_list = data['data'];

                vm.titleImage = vm.api+'image/'+vm.news_list[0].NewsId+'.jpg';
                vm.titleNews = vm.news_list[0].Title;

                vm.firstNew.ReadCount = vm.news_list[0].ReadCount;
                vm.firstNew.WordCount = vm.news_list[0].WordCount;
                vm.firstNew.HardWeight = vm.news_list[0].HardWeight;
                vm.firstNew.Source = vm.news_list[0].Source;
                vm.firstNew.newid = vm.news_list[0].NewsId;


                for(index in data['data'])
                {
                    vm.news_list[index].image =  vm.api+'image/'+vm.news_list[index].NewsId+'_s.jpg';
                }

                console.log(vm.news_list);

                vm.loading = false;

            }, function (err_data) {

            })
        },
        onRefresh: function () {
            /*
             return new Promise(function (resolve, reject) {
             setTimeout(function () {
             resolve();
             }, 1000);

             });
             */
            console.log("onRefresh");
        },
        clickTitle: function (item) {

        }
    }

});