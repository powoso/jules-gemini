document.addEventListener('DOMContentLoaded', () => {
    window.fetchFeed();
});

let currentSource = 'all';

// Expose setSource and fetchFeed to global scope
window.setSource = function(source) {
    currentSource = source;

    // Update button styles
    const buttons = ['btn-all', 'btn-reddit', 'btn-twitter'];
    buttons.forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (btn) {
            if (btnId === `btn-${source}`) {
                btn.classList.remove('hover:bg-gray-700', 'text-gray-400');
                btn.classList.add('bg-blue-600', 'text-white');
            } else {
                btn.classList.add('hover:bg-gray-700', 'text-gray-400');
                btn.classList.remove('bg-blue-600', 'text-white');
            }
        }
    });

    window.fetchFeed();
};

window.fetchFeed = async function() {
    const container = document.getElementById('feed-container');
    const loader = document.getElementById('loader');
    const errorMsg = document.getElementById('error-message');
    const refreshIcon = document.getElementById('refresh-icon');

    if (container) container.innerHTML = '';
    if (loader) loader.classList.remove('hidden');
    if (errorMsg) errorMsg.classList.add('hidden');
    if (refreshIcon) refreshIcon.classList.add('animate-spin');

    try {
        const url = `/api/feed?source=${currentSource}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const posts = await response.json();

        if (!posts || posts.length === 0) {
            if (container) container.innerHTML = '<div class="col-span-full text-center text-gray-500 py-10">No posts found.</div>';
        } else {
            posts.forEach(post => {
                const postElement = createPostElement(post);
                if (container) container.appendChild(postElement);
            });
        }

    } catch (error) {
        console.error('Error fetching feed:', error);
        if (errorMsg) {
            errorMsg.classList.remove('hidden');
            errorMsg.textContent = `Failed to load feed: ${error.message}`;
        }
    } finally {
        if (loader) loader.classList.add('hidden');
        if (refreshIcon) refreshIcon.classList.remove('animate-spin');
    }
};

function createPostElement(post) {
    const div = document.createElement('div');
    // Common styles
    div.className = 'bg-gray-800 rounded-lg overflow-hidden shadow-lg border border-gray-700 hover:border-gray-600 transition-all duration-300 flex flex-col h-full transform hover:-translate-y-1';

    let sourceIcon = '<i class="fas fa-globe text-gray-400"></i>';
    let sourceBadgeClass = 'bg-gray-700 text-gray-300 border-gray-600';

    if (post.source === 'reddit') {
        sourceIcon = '<i class="fab fa-reddit text-orange-500"></i>';
        sourceBadgeClass = 'bg-orange-900/30 text-orange-400 border-orange-500/30';
    } else if (post.source === 'twitter') {
        sourceIcon = '<i class="fab fa-twitter text-blue-400"></i>';
        sourceBadgeClass = 'bg-blue-900/30 text-blue-400 border-blue-400/30';
    }

    const timestamp = post.timestamp ? post.timestamp : '';
    const formattedTime = formatTime(timestamp);

    // Header HTML
    const headerHtml = `
        <div class="p-4 flex items-center justify-between border-b border-gray-700 bg-gray-800/50">
            <div class="flex items-center space-x-3 min-w-0">
                <div class="w-10 h-10 rounded-full overflow-hidden bg-gray-700 flex-shrink-0 border border-gray-600">
                    <img src="${post.avatar_url || 'https://via.placeholder.com/40'}" alt="${post.author}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/40?text=?'">
                </div>
                <div class="min-w-0 flex-1">
                    <h3 class="font-bold text-sm text-gray-200 truncate pr-2" title="${post.author}">${post.author}</h3>
                    <div class="text-xs text-gray-500 truncate" title="${timestamp}">${formattedTime}</div>
                </div>
            </div>
            <div class="flex-shrink-0 px-2 py-1 rounded text-xs font-semibold flex items-center gap-2 border ${sourceBadgeClass}">
                ${sourceIcon}
                <span class="uppercase tracking-wider hidden sm:inline">${post.source}</span>
            </div>
        </div>
    `;

    // Media HTML
    let mediaHtml = '';
    if (post.media_url) {
        mediaHtml = `
            <div class="relative w-full bg-black aspect-video flex items-center justify-center overflow-hidden group border-b border-gray-700">
                <img src="${post.media_url}" alt="Post Media" class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-105" loading="lazy" onerror="this.parentElement.style.display='none'">
            </div>
        `;
    }

    // Content HTML
    const contentHtml = `
        <div class="p-4 flex-grow">
            <div class="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap break-words">${linkify(post.content)}</div>
        </div>
    `;

    // Footer HTML
    const footerHtml = `
        <div class="p-3 bg-gray-900/50 border-t border-gray-700 mt-auto flex justify-end">
            <a href="${post.url}" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:text-blue-300 text-xs font-medium flex items-center gap-1 transition-colors hover:underline">
                View Original <i class="fas fa-external-link-alt"></i>
            </a>
        </div>
    `;

    div.innerHTML = headerHtml + mediaHtml + contentHtml + footerHtml;
    return div;
}

function linkify(text) {
    if (!text) return '';
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:underline break-all" onclick="event.stopPropagation()">${url}</a>`;
    });
}

function formatTime(timestamp) {
    if (!timestamp) return '';
    try {
        const date = new Date(timestamp);
        if (isNaN(date.getTime())) return timestamp;

        const now = new Date();
        const diff = (now - date) / 1000;

        if (diff < 60) return 'Just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        return date.toLocaleDateString();
    } catch (e) {
        return timestamp;
    }
}
