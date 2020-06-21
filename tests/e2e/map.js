// describe('Map', function () {
//     it('loads correctly and allows to zoom in and out', () => {
//         cy.visit('/');

//         // Check if the map is loaded
//         cy.get('.esri-view-root').should("be.visible");

//         // Check if zooming in and out works
//         cy.get('div[title*="Zoom in"]').click();
//         // cy.get('#coordsWidget').contains("Zoom 3");

//         cy.get('div[title*="Zoom out"]').click();
//         // cy.get('#coordsWidget').contains("Zoom 2");
//     });

//     it('has working nav menu', () => {
//         cy.visit('/');

//         // Check if navigation works. Hard to check an actual
//         // map change since it's embedded component with closed
//         // change logic
//         cy.get('#myNav').should('be.not.visible');
//         cy.get('.open').click();
//         cy.get('#myNav').should('be.visible');
//         cy.get("#2015").click({force: true});
//     })
// });