// Add noindex for pages.dev domains only
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const hostname = url.hostname;

  const response = await next();

  // Only modify HTML responses on pages.dev
  if (hostname.includes('pages.dev')) {
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      let html = await response.text();
      // Replace existing robots meta or add noindex
      if (html.includes('name="robots"')) {
        html = html.replace(
          /<meta name="robots" content="[^"]*">/,
          '<meta name="robots" content="noindex, nofollow">'
        );
      } else {
        html = html.replace(
          '<head>',
          '<head>\n    <meta name="robots" content="noindex, nofollow">'
        );
      }
      return new Response(html, {
        status: response.status,
        headers: response.headers
      });
    }
  }

  return response;
}
