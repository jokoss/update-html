// Services Application - Main JavaScript Logic
class ServicesApp {
    constructor() {
        this.currentFilter = 'all';
        this.currentSort = 'popular';
        this.currentView = 'grid';
        this.searchQuery = '';
        this.filteredServices = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadServices();
        this.animateCounters();
        this.setupIntersectionObserver();
    }

    bindEvents() {
        // Search functionality
        const searchInput = document.getElementById('serviceSearch');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.searchQuery = e.target.value.toLowerCase();
                this.filterAndRenderServices();
            }, 300));
        }

        // Category filters
        const categoryFilters = document.querySelectorAll('input[name="categoryFilter"]');
        categoryFilters.forEach(filter => {
            filter.addEventListener('change', (e) => {
                this.currentFilter = e.target.value;
                this.filterAndRenderServices();
                this.updateURL();
            });
        });

        // Sort options
        const sortSelect = document.getElementById('sortOptions');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.currentSort = e.target.value;
                this.filterAndRenderServices();
            });
        }

        // View mode toggle
        const viewModeInputs = document.querySelectorAll('input[name="viewMode"]');
        viewModeInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                this.currentView = e.target.value;
                this.renderServices(this.filteredServices);
            });
        });

        // Modal events
        const modal = document.getElementById('serviceDetailModal');
        if (modal) {
            modal.addEventListener('show.bs.modal', (e) => {
                const button = e.relatedTarget;
                const serviceId = button.getAttribute('data-service');
                const categoryId = button.getAttribute('data-category');
                this.loadServiceDetails(serviceId, categoryId);
            });
        }

        // Quote request button
        const quoteBtn = document.getElementById('requestQuoteBtn');
        if (quoteBtn) {
            quoteBtn.addEventListener('click', () => {
                this.handleQuoteRequest();
            });
        }

        // Handle URL parameters on load
        this.handleURLParameters();
    }

    loadServices() {
        this.showLoading();
        
        // Simulate loading delay for better UX
        setTimeout(() => {
            this.filteredServices = this.getAllServices();
            this.filterAndRenderServices();
            this.hideLoading();
        }, 500);
    }

    getAllServices() {
        const services = [];
        
        Object.keys(servicesData).forEach(categoryKey => {
            const category = servicesData[categoryKey];
            
            // Only add subcategory cards (remove main category cards)
            Object.keys(category.categories).forEach(subKey => {
                const subcategory = category.categories[subKey];
                services.push({
                    type: 'subcategory',
                    id: `${categoryKey}-${subKey}`,
                    title: subcategory.name,
                    description: subcategory.description,
                    icon: subcategory.icon,
                    color: category.color,
                    testCount: subcategory.tests.length,
                    turnaround: this.getAverageTurnaround(subcategory.tests),
                    popularity: category.popularity - 10,
                    tests: subcategory.tests,
                    category: categoryKey,
                    subcategory: subKey
                });
            });
        });

        return services;
    }

    filterAndRenderServices() {
        let filtered = this.getAllServices();

        // Apply category filter
        if (this.currentFilter !== 'all') {
            filtered = filtered.filter(service => service.category === this.currentFilter);
        }

        // Apply search filter
        if (this.searchQuery) {
            filtered = filtered.filter(service => {
                const searchText = `${service.title} ${service.description} ${service.subtitle || ''}`.toLowerCase();
                const keywords = searchKeywords[service.category] || [];
                const keywordMatch = keywords.some(keyword => keyword.includes(this.searchQuery));
                return searchText.includes(this.searchQuery) || keywordMatch;
            });
        }

        // Apply sorting
        filtered = this.sortServices(filtered);

        this.filteredServices = filtered;
        this.showCategoryDescription();
        this.renderServices(filtered);
        this.updateResultsCount(filtered.length);
    }

    sortServices(services) {
        switch (this.currentSort) {
            case 'alphabetical':
                return services.sort((a, b) => a.title.localeCompare(b.title));
            case 'turnaround':
                return services.sort((a, b) => {
                    const aTurnaround = this.parseTurnaround(a.turnaround);
                    const bTurnaround = this.parseTurnaround(b.turnaround);
                    return aTurnaround - bTurnaround;
                });
            case 'popular':
            default:
                return services.sort((a, b) => b.popularity - a.popularity);
        }
    }

    renderServices(services) {
        const container = document.getElementById('servicesContainer');
        const noResults = document.getElementById('noResults');
        
        if (!container) return;

        if (services.length === 0) {
            container.innerHTML = '';
            noResults.style.display = 'block';
            return;
        }

        noResults.style.display = 'none';
        
        if (this.currentView === 'grid') {
            this.renderGridView(services, container);
        } else {
            this.renderListView(services, container);
        }

        // Add animation to cards
        this.animateCards();
    }

    renderGridView(services, container) {
        const cardsHTML = services.map(service => this.createServiceCard(service)).join('');
        container.innerHTML = cardsHTML;
        container.className = 'row g-4';
    }

    renderListView(services, container) {
        const cardsHTML = services.map(service => this.createServiceCard(service, true)).join('');
        container.innerHTML = cardsHTML;
        container.className = 'row g-3';
    }

    createServiceCard(service, isListView = false) {
        const colClass = isListView ? 'col-12' : 'col-lg-4 col-md-6';
        const cardClass = isListView ? 'service-card list-view' : 'service-card';
        
        return `
            <div class="${colClass}">
                <div class="${cardClass}" data-aos="fade-up" data-aos-delay="${Math.random() * 200}">
                    ${isListView ? this.createListViewContent(service) : this.createGridViewContent(service)}
                </div>
            </div>
        `;
    }

    createGridViewContent(service) {
        return `
            <div class="card-body text-center">
                <div class="service-icon">
                    <img src="./assets/img/services/icons/${service.icon}" alt="${service.title}" />
                </div>
                <h3 class="card-title">${service.title}</h3>
                ${service.subtitle ? `<p class="text-muted small mb-2">${service.subtitle}</p>` : ''}
                <p class="card-text">${service.description}</p>
                
                <div class="service-tags">
                    ${service.popularTests ? service.popularTests.map(test => 
                        `<span class="service-tag">${test}</span>`
                    ).join('') : ''}
                </div>
                
                <div class="service-stats">
                    <div class="service-stat">
                        <span class="service-stat-value">${service.testCount}</span>
                        <span class="service-stat-label">Tests</span>
                    </div>
                    <div class="service-stat">
                        <span class="service-stat-value">${service.turnaround}</span>
                        <span class="service-stat-label">Turnaround</span>
                    </div>
                </div>
                
                <div class="mt-3">
                    <button class="btn btn-primary btn-sm me-2" 
                            data-bs-toggle="modal" 
                            data-bs-target="#serviceDetailModal"
                            data-service="${service.id}"
                            data-category="${service.category}">
                        View Details
                    </button>
                    <button class="btn btn-outline-primary btn-sm" 
                            onclick="requestQuote('${service.id}')">
                        Get Quote
                    </button>
                </div>
            </div>
        `;
    }

    createListViewContent(service) {
        return `
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-auto">
                        <div class="service-icon">
                            <img src="./assets/img/services/icons/${service.icon}" alt="${service.title}" />
                        </div>
                    </div>
                    <div class="col">
                        <h4 class="card-title mb-1">${service.title}</h4>
                        ${service.subtitle ? `<p class="text-muted small mb-2">${service.subtitle}</p>` : ''}
                        <p class="card-text mb-2">${service.description}</p>
                        <div class="service-tags">
                            ${service.popularTests ? service.popularTests.map(test => 
                                `<span class="service-tag">${test}</span>`
                            ).join('') : ''}
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="text-end">
                            <div class="mb-2">
                                <small class="text-muted">${service.testCount} tests • ${service.turnaround}</small>
                            </div>
                            <button class="btn btn-primary btn-sm me-2" 
                                    data-bs-toggle="modal" 
                                    data-bs-target="#serviceDetailModal"
                                    data-service="${service.id}"
                                    data-category="${service.category}">
                                View Details
                            </button>
                            <button class="btn btn-outline-primary btn-sm" 
                                    onclick="requestQuote('${service.id}')">
                                Get Quote
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    loadServiceDetails(serviceId, categoryId) {
        const modalTitle = document.getElementById('serviceDetailModalLabel');
        const modalContent = document.getElementById('serviceDetailContent');
        
        if (!modalTitle || !modalContent) return;

        const service = this.filteredServices.find(s => s.id === serviceId);
        if (!service) return;

        modalTitle.textContent = service.title;
        
        let detailsHTML = `
            <div class="row mb-4">
                <div class="col-md-8">
                    <h5>${service.subtitle || service.title}</h5>
                    <p class="lead">${service.description}</p>
                </div>
                <div class="col-md-4 text-md-end">
                    <div class="service-icon mx-auto mx-md-0">
                        <img src="./assets/img/services/icons/${service.icon}" alt="${service.title}" />
                    </div>
                </div>
            </div>
        `;

        if (service.tests && service.tests.length > 0) {
            detailsHTML += '<h6 class="mb-3">Available Test Packages</h6>';
            service.tests.forEach(test => {
                detailsHTML += `
                    <div class="test-package" onclick="selectTestPackage(this)">
                        <div class="test-package-header">
                            <h6 class="test-package-title">${test.name}</h6>
                        </div>
                        <p class="test-package-description">${test.description}</p>
                        <div class="row">
                            <div class="col-md-8">
                                <ul class="test-package-features">
                                    ${test.features.map(feature => `<li>${feature}</li>`).join('')}
                                </ul>
                            </div>
                            <div class="col-md-4 text-md-end">
                                <small class="text-muted">
                                    <i class="bx bx-time me-1"></i>${test.turnaround}
                                </small>
                            </div>
                        </div>
                    </div>
                `;
            });
        }

        modalContent.innerHTML = detailsHTML;
    }

    // Utility functions
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    getAverageTurnaround(tests) {
        if (!tests || tests.length === 0) return '5-7 days';
        
        const turnarounds = tests.map(test => this.parseTurnaround(test.turnaround));
        const average = turnarounds.reduce((sum, days) => sum + days, 0) / turnarounds.length;
        
        return `${Math.floor(average)}-${Math.ceil(average + 2)} days`;
    }

    parseTurnaround(turnaround) {
        const match = turnaround.match(/(\d+)/);
        return match ? parseInt(match[1]) : 5;
    }

    animateCounters() {
        const counters = document.querySelectorAll('.counter[data-target]');
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;
            
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    counter.textContent = target;
                    clearInterval(timer);
                } else {
                    counter.textContent = Math.floor(current);
                }
            }, 16);
        });
    }

    animateCards() {
        const cards = document.querySelectorAll('.service-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, { threshold: 0.1 });

        // Observe service cards as they're added
        const observeCards = () => {
            document.querySelectorAll('.service-card:not(.observed)').forEach(card => {
                observer.observe(card);
                card.classList.add('observed');
            });
        };

        // Initial observation
        setTimeout(observeCards, 100);
        
        // Re-observe after filtering
        document.addEventListener('servicesRendered', observeCards);
    }

    showLoading() {
        const loading = document.getElementById('servicesLoading');
        const container = document.getElementById('servicesContainer');
        if (loading) loading.style.display = 'block';
        if (container) container.innerHTML = '';
    }

    hideLoading() {
        const loading = document.getElementById('servicesLoading');
        if (loading) loading.style.display = 'none';
    }

    showCategoryDescription() {
        const categoryDescriptionEl = document.getElementById('categoryDescription');
        const categoryTitleEl = document.getElementById('categoryTitle');
        const categorySubtitleEl = document.getElementById('categorySubtitle');
        const categoryDescriptionTextEl = document.getElementById('categoryDescriptionText');
        
        if (!categoryDescriptionEl || !categoryTitleEl || !categorySubtitleEl || !categoryDescriptionTextEl) return;
        
        if (this.currentFilter === 'all' || this.searchQuery) {
            categoryDescriptionEl.style.display = 'none';
            return;
        }
        
        const categoryData = servicesData[this.currentFilter];
        if (!categoryData) {
            categoryDescriptionEl.style.display = 'none';
            return;
        }
        
        categoryTitleEl.textContent = categoryData.title;
        categorySubtitleEl.textContent = categoryData.subtitle;
        categoryDescriptionTextEl.textContent = categoryData.description;
        categoryDescriptionEl.style.display = 'block';
    }

    updateResultsCount(count) {
        // Update filter buttons with counts if needed
        const totalCount = this.getAllServices().length;
        console.log(`Showing ${count} of ${totalCount} services`);
    }

    handleURLParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const category = urlParams.get('category');
        const search = urlParams.get('search');
        
        if (category && category !== 'all') {
            const categoryInput = document.getElementById(category);
            if (categoryInput) {
                categoryInput.checked = true;
                this.currentFilter = category;
            }
        }
        
        if (search) {
            const searchInput = document.getElementById('serviceSearch');
            if (searchInput) {
                searchInput.value = search;
                this.searchQuery = search.toLowerCase();
            }
        }
    }

    updateURL() {
        const params = new URLSearchParams();
        if (this.currentFilter !== 'all') {
            params.set('category', this.currentFilter);
        }
        if (this.searchQuery) {
            params.set('search', this.searchQuery);
        }
        
        const newURL = params.toString() ? `${window.location.pathname}?${params.toString()}` : window.location.pathname;
        window.history.replaceState({}, '', newURL);
    }

    handleQuoteRequest() {
        // Redirect to contact page
        window.location.href = './contact-us/index.html';
    }
}

// Global functions for inline event handlers
function selectTestPackage(element) {
    // Remove selected class from all packages
    document.querySelectorAll('.test-package').forEach(pkg => {
        pkg.classList.remove('selected');
    });
    
    // Add selected class to clicked package
    element.classList.add('selected');
}

function requestQuote(serviceId) {
    // Redirect to contact page with service information
    window.location.href = './contact-us/index.html';
}

function clearFilters() {
    // Reset all filters
    document.getElementById('all').checked = true;
    document.getElementById('serviceSearch').value = '';
    document.getElementById('sortOptions').value = 'popular';
    
    // Trigger app to reload services
    if (window.servicesApp) {
        window.servicesApp.currentFilter = 'all';
        window.servicesApp.searchQuery = '';
        window.servicesApp.currentSort = 'popular';
        window.servicesApp.filterAndRenderServices();
        window.servicesApp.updateURL();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.servicesApp = new ServicesApp();
});

// Handle browser back/forward buttons
window.addEventListener('popstate', () => {
    if (window.servicesApp) {
        window.servicesApp.handleURLParameters();
        window.servicesApp.filterAndRenderServices();
    }
});
