module.exports = {
    title: "David Banville",
    description: "Some guy's website",
    themeConfig: {
        nav: [
            {text: 'Page 1', link: 'page1.md'},
            {text: 'Page 2', link: 'page2.md'},
        ],
        sidebar: [
            './',
            ['./page1','Page 1'],
            ['./page2','Page 2'],
        ]
    }
}