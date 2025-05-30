from django import template
from product.models import ProductStatusType, ProductModel,WishlistProductModel

register = template.Library()

@register.inclusion_tag("includes/latest-products.html",takes_context=True)
def show_latest_products(context):
    request = context.get("request")
    latest_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value).distinct().order_by("-created_date")[:8]
    wishlist_items = WishlistProductModel.objects.filter(user=request.user).values_list("product__id",flat=True) if request.user.is_authenticated else []
    return {"latest_products": latest_products,"request":request,"wishlist_items":wishlist_items}

@register.inclusion_tag("includes/similar-products.html",takes_context=True)
def show_similar_products(context,product):
    request = context.get("request")
    product_categories= product.category.all()
    similar_prodcuts = ProductModel.objects.filter(
        status=ProductStatusType.publish.value,category__in=product_categories).distinct().exclude(id=product.id).order_by("-created_date")[:4]
    wishlist_items =  WishlistProductModel.objects.filter(user=request.user).values_list("product__id",flat=True) if request.user.is_authenticated else []
    return {"similar_prodcuts": similar_prodcuts,"request":request,"wishlist_items":wishlist_items}

@register.inclusion_tag("includes/most-viewed-products.html", takes_context=True)
def show_most_viewed_products(context):
    request = context.get("request")

    # دریافت ۸ محصول پربازدید که منتشر شده‌اند
    most_viewed_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value
    ).order_by("-views")[:8]

    # بررسی محصولات در لیست علاقه‌مندی‌های کاربر
    wishlist_items = WishlistProductModel.objects.filter(user=request.user).values_list(
        "product__id", flat=True) if request.user.is_authenticated else []

    return {
        "most_viewed_products": most_viewed_products,
        "request": request,
        "wishlist_items": wishlist_items
    }

@register.inclusion_tag("includes/discounted-products.html", takes_context=True)
def show_discounted_products(context):
    request = context.get("request")
    
    # دریافت محصولات دارای تخفیف که منتشر شده‌اند
    discounted_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value, discount_percent__gt=0
    ).order_by("-created_date")[:8]

    # دریافت لیست محصولات موجود در لیست علاقه‌مندی‌های کاربر (در صورت لاگین بودن)
    wishlist_items = WishlistProductModel.objects.filter(
        user=request.user
    ).values_list("product__id", flat=True) if request.user.is_authenticated else []

    return {
        "discounted_products": discounted_products,
        "request": request,
        "wishlist_items": wishlist_items
    }