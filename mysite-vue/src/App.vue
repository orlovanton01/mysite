<script setup>
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container">
        <a class="navbar-brand" href="#">Агрегатор</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Переключатель навигации">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Главная</a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Войти
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Вход</a></li>
                <li><a class="dropdown-item" href="#">Регистрация</a></li>
              </ul>
            </li>
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Сравнение</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Избранное</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container" id="main">
      <RouterView />
  </div>
</template>

<style>
#main{
  padding-top: 2%;
}
*{
  font-size:14px;
}
</style>
