<template>
  <n-message-provider>
  <n-config-provider :theme="darkTheme" :locale="zhCN" :date-locale="dateZhCN">
    <n-space vertical>
      <n-form
        inline
        :label-width="200"
        :model="formValue"
        :rules="rules"
        ref="formRef"
      >
        <n-form-item label="书名" path="phone">
          <n-input placeholder="书名" v-model:value="formValue.book_name" />
        </n-form-item>
        <n-form-item>
          <n-button @click="handleValidateClick">添加</n-button>
        </n-form-item>
      </n-form>

<!--      <n-date-picker />-->
      <n-data-table :columns="columns" :data="data" :pagination="pagination" />
    </n-space>
  </n-config-provider>
  </n-message-provider>
</template>


<script>
  import {NConfigProvider, NInput, NSpace, NDataTable} from 'naive-ui'
  // theme
  import { createTheme, inputDark, dataTableDark, buttonDark } from 'naive-ui'
  // locale & dateLocale
  import { NForm, NFormItem  } from 'naive-ui'
  import { zhCN, dateZhCN } from 'naive-ui'
  import { h, defineComponent } from 'vue'
  import { NButton, useMessage } from 'naive-ui'
  // import { Ntag } from 'naive-ui'
  import { NMessageProvider } from 'naive-ui'
  import { ref, onMounted } from 'vue'
  import axios from 'axios';

  const createColumns = ({ sendMail }) => {
    return [
      {
        title: '编号',
        key: 'pk',
      },
      {
        title: '书名',
        key: 'book_name'
      },
      {
        title: '添加时间',
        key: 'add_time'
      },
      // {
      //   title: '',
      //   key: 'fields',
      //   children: [
      //     {
      //       title: '书名',
      //       key: 'book_name',
      //     },
      //     {
      //       title: '添加时间',
      //       key: 'add_time',
      //     }
      //   ]
      // },
      // {
      //   title: 'Tags',
      //   key: 'tags',
      //   render (row) {
      //     const tags = row.tags.map((tagKey) => {
      //       return h(
      //         NTag,
      //         {
      //           style: {
      //             marginRight: '6px'
      //           },
      //           type: 'info'
      //         },
      //         {
      //           default: () => tagKey
      //         }
      //       )
      //     })
      //     return tags
      //   }
      // },
      {
        title: 'Action',
        key: 'actions',
        render (row) {
          return h(
            NButton,
            {
              size: 'small',
              onClick: () => sendMail(row)
            },
            { default: () => 'read' }
          )
        }
      }
    ]
  }

  // const createData = () => [
  //   {
  //     pk: 0,
  //     book_name: 'John Brown',
  //     add_time: 32,
  //     // address: 'New York No. 1 Lake Park',
  //     // tags: ['nice', 'developer']
  //   },
  //   {
  //     pk: 1,
  //     book_name: 'Jim Green',
  //     add_time: 42,
  //     // address: 'London No. 1 Lake Park',
  //     // tags: ['wow']
  //   },
  //   {
  //     pk: 2,
  //     book_name: 'Joe Black',
  //     add_time: 32,
  //     // address: 'Sidney No. 1 Lake Park',
  //     // tags: ['cool', 'teacher']
  //   }
  // ]

  const fetchAllBooks = (books) => {
    axios
      .get('http://127.0.0.1:8000/api/show_books')
      .then(function (response) {
        // console.log(response);
        if (response.data.error_num == 0) {
          // console.log(Object.values(response.data.list));
          let tmp = response.data.list
          for (let i=0; i < tmp.length; i++) {
            for (let k in tmp[i]["fields"]) {
              tmp[i][k] = tmp[i]["fields"][k]
            }
            delete tmp[i]["fields"]
          }
          // console.log(tmp)
          books.value = tmp
          // console.log(books)
        }
      })
  }
  const addBook = (nameRef) => {
    // console.log(nameRef)
    axios
      .get('http://127.0.0.1:8000/api/add_book?book_name=' + nameRef.model.book_name)
      .then(function (response) {
        // if (response.data.error_num == 0) {
        //
        // }
        console.log(response)
        // console.log(nameRef)
      })
  }
  export default defineComponent({
    components: {
      NConfigProvider,
      NInput,
      // NDatePicker,
      NSpace,
      NDataTable,
      NMessageProvider,
      NForm,
      NFormItem,
      NButton
    },
    setup() {
      const message = useMessage()
      const books = ref([])
      const getAllBooks = async () => {
        await fetchAllBooks(books)
      }
      onMounted(getAllBooks)
      const formRef = ref(null)

      return {
        // data: createData(),
        data: books,
        columns: createColumns({
          sendMail (rowData) {
            message.info('read ' + rowData.book_name)
          }
        }),
        pagination: {
          pageSize: 10
        },
        darkTheme: createTheme([inputDark, dataTableDark, buttonDark ]),
        zhCN,
        dateZhCN,
        getAllBooks,
        formRef,
        formValue: ref({
          book_name: ''
        }),
        rules: {
          book_name: {
            required: true,
            message: '请输入书名',
            trigger: ['input']
          }
        },
        handleValidateClick () {
          formRef.value.validate((errors) => {
            if (!errors) {
              // console.log(formRef)
              addBook(formRef.value)
              message.success('add')
              getAllBooks()
            } else {
              console.log(errors)
              message.error('Invalid')
            }
          })
        }
      }
    }
  })
</script>

<style>
  body {
    background: black;
  }
</style>
