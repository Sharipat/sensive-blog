from django.db import models
from django.db.models import Count, Prefetch
from django.urls import reverse
from django.contrib.auth.models import User


class PostQuerySet(models.QuerySet):

    def popular(self):
        popular_posts = self.annotate(
            num_likes=Count('likes', distinct=True)).\
            order_by('-num_likes')
        return popular_posts

    def fetch_with_comments_count(self):
        posts_with_comments = Post.objects.filter(
            id__in=self
        ).annotate(
            comments_count=Count('comments')
        )
        post_ids_and_comments = dict(
            posts_with_comments.values_list('id', 'comments_count')
        )
        for post in self:
            post.comments_count = post_ids_and_comments[post.id]
        return self

    def fetch_posts_count_for_tags(self):
        return self.prefetch_related(
            Prefetch(
                'tags',
                queryset=Tag.objects.annotate(posts_count=Count('posts')),
                to_attr='tags_with_posts'))

    def fresh(self):
        fresh_posts = self.order_by('-published_at')
        return fresh_posts


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Текст')
    slug = models.SlugField('Название в виде url', max_length=200)
    image = models.ImageField('Картинка')
    published_at = models.DateTimeField('Дата и время публикации')
    objects = PostQuerySet.as_manager()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='authors',
        limit_choices_to={'is_staff': True})
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        verbose_name='Кто лайкнул',
        blank=True)
    tags = models.ManyToManyField(
        'Tag',
        related_name='posts',
        verbose_name='Теги')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args={'slug': self.slug})

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class TagQuerySet(models.QuerySet):

    def popular(self):
        popular_tags = self.annotate(
            posts_count=Count('posts', distinct=True)).\
            order_by('-posts_count')
        return popular_tags

    def fetch_with_posts_count(self):
        ids = [tag.id for tag in self]
        tags_with_posts = Tag.objects.filter(
            id__in=ids).annotate(
            posts_count=Count('posts'))
        ids_and_posts = tags_with_posts.values_list('id', 'posts_count')
        count_for_id = dict(ids_and_posts)
        for tag in self:
            tag.posts_count = count_for_id[tag.id]
        return self


class Tag(models.Model):
    title = models.CharField('Тег', max_length=20, unique=True)
    objects = TagQuerySet.as_manager()

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.lower()

    def get_absolute_url(self):
        return reverse('tag_filter', args={'tag_title': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост, к которому написан')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_authors',
        verbose_name='Автор')

    text = models.TextField('Текст комментария')
    published_at = models.DateTimeField('Дата и время публикации')

    def __str__(self):
        return f'{self.author.username} under {self.post.title}'

    class Meta:
        ordering = ['published_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
