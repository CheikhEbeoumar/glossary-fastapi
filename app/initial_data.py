def get_initial_terms():
    return [
        {
            "name": "Server-Side Rendering (SSR)",
            "description": "Technique where the HTML is generated on the server for each request, providing fully rendered HTML to the client",
            "rendering_type": "SSR",
            "frameworks": ["Next.js", "Nuxt.js", "Angular Universal", "Laravel", "Django", "Ruby on Rails"],
            "use_cases": ["Dynamic content", "SEO-critical applications", "Personalized pages", "E-commerce product pages"],
            "advantages": ["Better SEO", "Fast initial load", "Social media sharing", "Consistent performance"],
            "disadvantages": ["Server load", "TTFB can be slower", "More complex caching", "Server costs"]
        },
        {
            "name": "Static Site Generation (SSG)",
            "description": "Pre-renders pages at build time, serving static HTML files that can be cached and delivered via CDN",
            "rendering_type": "SSG",
            "frameworks": ["Next.js", "Gatsby", "VuePress", "Jekyll", "Hugo", "Eleventy"],
            "use_cases": ["Blogs", "Documentation", "Marketing sites", "Portfolios", "News sites"],
            "advantages": ["Excellent performance", "Great SEO", "Easy CDN caching", "High security", "Low server costs"],
            "disadvantages": ["Build time grows with content", "Not suitable for highly dynamic content", "Real-time updates challenging"]
        },
        {
            "name": "Client-Side Rendering (CSR)",
            "description": "Renders content entirely in the browser using JavaScript after downloading the necessary code",
            "rendering_type": "CSR",
            "frameworks": ["React", "Vue.js", "Angular", "Svelte", "Ember.js"],
            "use_cases": ["Web applications", "Dashboards", "Admin panels", "Highly interactive apps", "SPAs"],
            "advantages": ["Rich interactivity", "Fast navigation after load", "Better developer experience", "Offline capabilities"],
            "disadvantages": ["Poor SEO", "Slow initial load", "Blank page issue", "JavaScript dependency"]
        },
        {
            "name": "Incremental Static Regeneration (ISR)",
            "description": "Update static content after build-time without rebuilding entire site, combining benefits of SSG and SSR",
            "rendering_type": "ISR",
            "frameworks": ["Next.js"],
            "use_cases": ["E-commerce product pages", "News sites", "User-generated content", "Blogs with comments"],
            "advantages": ["Best of SSG and SSR", "Scalable", "Fast with fresh content", "Reduced build times"],
            "disadvantages": ["Next.js specific", "Complex cache invalidation", "Vendor lock-in"]
        },
        {
            "name": "Hydration",
            "description": "Process of making static HTML interactive on the client side by attaching event listeners and state",
            "rendering_type": "SSR",
            "frameworks": ["Next.js", "Nuxt.js", "SvelteKit", "Gatsby"],
            "use_cases": ["SSR applications", "Progressive enhancement", "Interactive static sites"],
            "advantages": ["Fast initial load", "SEO friendly", "Progressive enhancement"],
            "disadvantages": ["Hydration mismatch", "JavaScript bundle required", "Double data fetching"]
        },
        {
            "name": "Streaming Server-Side Rendering",
            "description": "Technique that streams HTML to the client as it's being generated on the server",
            "rendering_type": "SSR",
            "frameworks": ["Next.js", "Qwik", "React 18"],
            "use_cases": ["Large pages", "Slow data dependencies", "Dashboard applications"],
            "advantages": ["Faster Time to First Byte", "Better perceived performance", "Progressive loading"],
            "disadvantages": ["Complex implementation", "Limited framework support", "Browser compatibility"]
        }
    ]