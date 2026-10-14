# Dựng lại trang web

Trang `index.html` được sinh tự động từ `tuyen-tap.md`. Sau khi sửa file markdown, chạy lại từ thư mục gốc repo:

```
pip install markdown
python3 david-pawson-unlocking-the-bible/_build/build.py david-pawson-unlocking-the-bible/tuyen-tap.md david-pawson-unlocking-the-bible/index.html david-pawson-unlocking-the-bible/_build/tpl.html
```

Hình minh hoạ nằm trong `figures.py`. Trong `tuyen-tap.md`, dòng `<!-- fig:ten -->` chèn hình `ten` vào đúng chỗ đó; khối `<!-- fig:ten --> ... <!-- /fig -->` thì trên trang web được thay hẳn bằng hình (file markdown vẫn giữ chữ).
